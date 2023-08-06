import os
import sys
import traceback

import allure
import copy
import time
import inspect
import requests
import json
from allure_commons._allure import Attach
from allure import attachment_type
from urllib.parse import urlencode
from . import api
from ..common import config, constant, logger


class Attachs(Attach):

    def __init__(self, *args, **kwargs):
        super().__call__(*args, **kwargs)

    def __enter__(self):
        ...

    def __exit__(self, exc, value, tb):
        ...


class MyEncoder(json.JSONEncoder):

    def default(self, o):
        if isinstance(o, bytes):
            return str(o, encoding='utf-8')
        elif isinstance(o, str) is False and isinstance(o, list) is False and isinstance(o, dict) is False:
            return str(o)
        return super().default(o)


class requestBase(api.Api):

    def __init__(self):
        super().__init__()
        self.setup_hook_list = []
        self.teardown_hook_list = []
        self.except_hook_list = []
        self.logger = logger
        self.hook_switch = {}
        self.session = requests.Session()
        self.base_url = None # 域名
        self.catch_response = False # locust的时候使用
        self.kwargs = {} # request配置文件内的参数

    def set_session(self, client):
        self.session = client

    def register_setup_hook(self, hook):
        """
        注册前置钩子
        :param hook:
        :return:
        """
        self.hook_switch[hook.__name__] = True
        self.setup_hook_list.append(hook)

    def register_except_hook(self, hook):
        """
        注册前置钩子
        :param hook:
        :return:
        """
        self.hook_switch[hook.__name__] = True
        self.except_hook_list.append(hook)

    def register_teardown_hook(self, hook):
        """
        注册后置钩子
        :param hook:
        :return:
        """
        self.hook_switch[hook.__name__] = True
        self.teardown_hook_list.append(hook)

    def get_url(self, path):
        """
            获取网址
        """
        assert self.base_url is not None, '未定义base_url'

        if self.base_url.endswith('/'):
            self.base_url = self.base_url[:-1]
        url = self.base_url + path
        return url

    def send(self, api_id, is_json=True, title=None, **kwargs):
        request = copy.deepcopy(self.get_api(api_id))
        print('api:', request)
        if title is not None:
            request['title'] = title
        request['params'] = kwargs.pop('params', {})
        if request['method'] == "GET":
            kwargs.pop('json', {})
            kwargs.pop('data', {})
        else:
            request['json'] = self.update_dic(request.get('json', {}), kwargs.pop('json', {}))
            request['data'] = self.update_dic(request.get('data', {}), kwargs.pop('data', {}))
        request['headers'] = self.update_dic(request.get('headers', {}), kwargs.pop('headers', {}))
        self.update_dic(request, kwargs)
        response = self.execute(request)
        if is_json is True:
            return response.json()
        return response

    def update_dic(self, start, end):
        '''
        Updater of multi-level dictionary.

        Last level value is unmergable.
        '''
        if start is None or start == {}:
            return end
        for k, v in end.items():
            if k not in start:
                start[k] = v
            elif isinstance(v, list) is True and isinstance(start[k], list):
                start[k] += v
            elif isinstance(v, dict) is True and isinstance(start[k], dict):
                start[k] = self.update_dic(start[k], end[k])
            else:
                start[k] = v
        return start

    def close_hook(self, key=None):
        if key is None:
            for k in self.hook_switch:
                self.hook_switch[k] = False
        elif key in self.hook_switch:
            self.hook_switch[key] = False
        else:
            raise TypeError(f'不存在的hook，hook列表:{self.hook_switch}')

    def open_hook(self, key=None):
        if key is None:
            for k in self.hook_switch:
                self.hook_switch[k] = True
        else:
            self.hook_switch[key] = True

    def execute(self, request) -> requests.Response:
        """
            发送请求
        """
        for hook in self.setup_hook_list:
            if self.hook_switch[hook.__name__] is True:
                self.excute_kwargs(hook, request)
        request['title'] = request.get('title') if request.get('title') is not None else request.get('path')
        _name = request['title'].format(**request)
        with allure.step(_name):
            allure.attach(json.dumps(request, cls=MyEncoder, sort_keys=True, ensure_ascii=False, indent=4, separators=(',', ':')),
                     name="请求体", attachment_type=attachment_type.JSON)
            self.logger.debug('发送请求：{}'.format(request['title']))
            try:
                response = self._excute(request)
            except Exception as e:
                for hook in self.except_hook_list:
                    if self.hook_switch[hook.__name__] is True:
                        response = self.excute_kwargs(hook, request, error=e)
                if len(self.except_hook_list) == 0:
                    raise TypeError(f'未定义except_hook异常，异常内容:{traceback.format_exc()}')
            for hook in self.teardown_hook_list:
                if self.hook_switch[hook.__name__] is True:
                    self.excute_kwargs(hook, request, response)
            return response

    def excute_kwargs(self, hook, request, response={}, error=None, num=0):
        kwarg = {}
        kwargs = {'request': request, 'excute': self._excute, 'error': error, 'response': response,
                  'session': self.session, 'kwargs': self.kwargs, 'num': num}
        for i in inspect.getfullargspec(hook).args:
            if i in ['self', 'cls'] or i not in kwargs:
                continue
            kwarg[i] = kwargs[i]
        try:
            logger.debug(f'执行hook：{hook}')
            return hook(**kwarg)
        except Exception as e:
            if num <= 3:
                for hook in self.except_hook_list:
                    if self.hook_switch[hook.__name__] is True:
                        return self.excute_kwargs(hook, request, error=e, num=num+1)
                if len(self.except_hook_list) == 0:
                    raise TypeError(f'未定义except_hook异常，异常内容:{traceback.format_exc()}')
            else:
                raise e

    def copy_request(self, request):
        new_request = {}
        if 'files' not in request:
            new_request = copy.deepcopy(request)
        else:
            for key in request:
                if key == 'files':
                    new_request['files'] = request['files']
                else:
                    new_request[key] = copy.deepcopy(request[key])
        return new_request

    def _excute(self, request) -> requests.Response:
        current_time = time.time()
        new_request = self.copy_request(request)
        new_request['url'] = self.get_url(new_request.get('path'))
        if 'path' in new_request:
            del new_request['path']
        new_request['verify'] = False
        if self.catch_response is True:
            new_request['url'] = new_request['url'] + '?' + urlencode(new_request['params'])
            new_request['name'] = new_request['title']
            del new_request['params']
            new_request['catch_response'] = True
        for i in ['id', 'title']:
            if i in new_request:
                del new_request[i]
        msg = '请求参数：method：{}，url：{}, \nparams:{}, headers:{}, \ndata:{}, json:{}'.format(new_request.get('method'),
                                                                    new_request.get('url'), new_request.get('params'),
                                            new_request.get('headers'), new_request.get('data'), new_request.get('json'))
        try:
            result = self.session.request(**new_request)
        except requests.exceptions.ConnectionError as e:
            self.logger.debug('{}, 入参:{}'.format(msg, new_request))
            raise e
        response = result.text.replace('\n', '').replace('\r', '').replace('  ', '')
        self.logger.debug('{}, \n返回：{},时间:{}, 状态码:{}'.format(msg, response, time.time() - current_time,
                                                             result.status_code))
        if self.catch_response is True:
            return result
        return result

    def qs_parse(self, data):
        for key in list(data.keys()):
            value = data[key]
            if type(value) == dict:
                del data[key]
                for _key in list(value.keys()):
                    data[key + '[' + _key + ']'] = value[_key]
            elif type(value) == list:
                del data[key]
                for _key in range(len(value)):
                    data[key + '[' + str(_key) + ']'] = value[_key]
