import random
import time
import os
import sys
from decimal import Decimal
import json_tools
import allure
import pytest
import time
import datetime
import random
from decimal import Decimal
import requests
from faker import Faker
from . import conf
from .data import tmp
from .common import config, constant, common
from .common import logger
from .common.common import NewDict
from .data.conversion import Conversion
from autoTestScheme.configuration.sql import MySql
from autoTestScheme.configuration.request import requestBase
from allure_commons.types import LabelType, LinkType


class fixture(object):
    def __init__(self):
        self.kwargs = {}
        self.args = ()
        self.wrapped_func = None

    def __iter__(self):
        return self

    def __next__(self):
        if self.wrapped_func is None:
            self.wrapped_func = self.wrapped(*self.args, **self.kwargs)
        _type = '前置' if conf.settings._end_session is False else '后置'
        logger.info(f'执行{_type}条件:{self.wrapped}')
        return next(self.wrapped_func, None)

    def __call__(self, obj):
        self.wrapped = obj
        conf.settings._fixture_list.append(self)
        return self.wrapped


class Base(object):

    logger: logger = logger
    tag_func_list = {}
    settings: conf.BaseDynaconf = conf.settings

    @pytest.fixture()
    def data_conversion(self, request):
        '''
            数据转换使用,将数据进行特殊转换
        '''
        if 'data' in list(request.node.funcargs.keys()):
            param = request.node.funcargs.get('data')
        else:
            param = request.getfixturevalue('data')
        if param.get('dependent') is not None:
            param['lastTmp'] = tmp.tmp.get_lastTmp(param.get('dependent'))
            param['dpTmp'] = tmp.tmp.get(param.get('dependent'))
        if 'client' in param:
            self.settings.current_request = getattr(self.settings, param['client'])
        param = self.conversion(param, 'assert')
        self.excute_dynamic(param.getdefault('allure', {}))
        if param != {}:
            allure.dynamic.title(param.get('title'))
            if param.get('story') is not None:
                allure.dynamic.story(param.get('story'))
            request.node.name = param.get('title')
        logger.info('开始运行用例:{}'.format(param.get('title')))
        logger.info(param)
        yield param

        if param.get('id') is not None:
            tmp.tmp.append_lastTmp(param.get('id'), param)

    @pytest.fixture(autouse=True)
    def data(self):
        ...

    @pytest.fixture(scope="session", autouse=True)
    def session_fixture(self):
        _fixture_list = []
        for i in conf.settings._fixture_list:
            i.args = (self,)
            _fixture_list.append(i)
        if self.settings._first_session is False:
            self.settings._first_session = True
            for i in _fixture_list:
                try:
                    next(i, None)
                except TypeError:
                    logger.error("请在前置方法内加入yield进行结尾")
        yield
        if self.settings._end_session is False:
            self.settings._end_session = True
            for i in _fixture_list:
                try:
                    next(i, None)
                except TypeError:
                    logger.error("请在前置方法内加入yield进行结尾")
            self.settings.execute_all_close_hook()

    @fixture()
    def start_hook_register(self):
        for name in conf.settings.__dir__():
            if name.startswith("request"):
                client = getattr(conf.settings, name)
                for j in client.kwargs.get('setup_hook', []):
                    self.logger.info('{}注册setup_hook：{}'.format(name, j))
                    client.register_setup_hook(self.get_func(j))
                for j in client.kwargs.get('teardown_hook', []):
                    self.logger.info('{}注册teardown_hook：{}'.format(name, j))
                    client.register_teardown_hook(self.get_func(j))
                for j in client.kwargs.get('except_hook', []):
                    self.logger.info('{}注册except_hook：{}'.format(name, j))
                    client.register_except_hook(self.get_func(j))
        yield

    def get_func(self, func):
        if func in dir(self):
            return eval('self.{}'.format(func))
        return False

    def conversion(self, param, *exclude):
        import copy
        tmp = {}
        new_param = copy.deepcopy(param)
        con = Conversion(self, new_param)
        con.re_dict(list(exclude))
        new_param = con.json
        new_param.update(tmp)
        return self.get_my_dict(new_param)

    def get_my_dict(self, param):
        '''
        将字典类添加一个新的获取方法(gets)，改方法可以一次性获取多个值
        @param param: 字典类
        @return: MyDict类
        '''
        return NewDict(param)

    def check_response(self, response, outs):
        '''
            数据对比，常用于在判断请求结果与预期的校验
        '''
        compare = json_tools.diff(outs, response)
        result = {'remove':[], 'add':[], 'replace':[]}
        for i in compare:
            _type = ''
            if 'remove' in list(i.keys()):
                _type = 'remove'
                i = i['remove']
            elif 'add' in list(i.keys()):
                _type = 'add'
                i = i['add']
            elif 'replace' in list(i.keys()):
                _type = 'replace'
                i['实际'] = i['value']
                i['预期'] = i['prev']
                i['路径'] = i['replace']
                if 'details' in i:
                    if i['details'] == 'type':
                        i['说明'] = '类型错误'
                    del i['details']
                del i['value']
                del i['prev']
                del i['replace']
            result[_type].append(i)
        if len(result['add']) > 0:
            self.logger.warning('校验的内容中增加的字段:{}'.format(' ; '.join(result['add'])))
        msg = []
        if len(result['remove']) > 0:
            msg.append("校验的内容中被删除的字段:{}".format(' ; '.join(result['remove'])))
        if len(result['replace']) > 0:
            msg.append("校验的内容中被修改的字段及内容:{}".format(result['replace']))
        assert len(msg) == 0, '比较结果:{},实际：{}，预期:{}'.format(';'.join([str(i) for i in msg]), response, outs)

    def check_inclusion_relation(self, a, b):
        '''
            a,b都是dict类型
            判断b是否包含a内的所有元素
        '''
        for i in list(a.items()):
            if i not in list(b.items()):
                self.logger.error('不包含元素:{},数据:\na:{},\nb:{}'.format(i, a, b))
                return False
        return True

    def excute_dynamic(self, param):
        dynamic_list = {}
        dynamic_list['issue'] = allure.dynamic.issue
        dynamic_list['label'] = allure.dynamic.label
        dynamic_list['link'] = allure.dynamic.link
        dynamic_list['testcase'] = allure.dynamic.testcase
        allure.dynamic.label('tag', conf.settings.run.env)
        for name, value in param.items():
            if name == 'label':
                for k, v in value.items():
                    allure.dynamic.label(k, v)
            elif name in ['issue', 'link', 'testcase', 'label']:
                if isinstance(value, list) is False:
                    logger.error('用例配置错误，{} 键的内容必须为列表'.format(name))
                else:
                    for a in value:
                        dynamic_list[name](a[0], name=a[1])

    def check_response_by_sql(self, response, outs):
        '''
            比较返回与数据库，与check_response的区别在于会将response与outs的key转换为下划线形式字符串
        '''
        response = common.dict_value_hump2underline(response)
        outs = common.dict_value_hump2underline(outs)
        return self.check_response(response, outs)

    def conver_decimal(self, data:dict) -> dict:
        """
        将字典内的Decimal类型字段转换未float
        @param data:
        @return:
        """
        for i in list(data.keys()):
            if type(data[i]) == Decimal:
                data[i] = float(data[i])
        return data


    @property
    def faker(self):
        return Faker(locale='zh_CN')

    def convert_uppercase(self, string):
        """
        将字符串转换成大写
        """
        return string.upper()

    @property
    def not_repeat_string(self):
        """
        获取不重复字符串
        @return:
        """
        return '{}_{}_{}'.format(''.join(random.sample('zyxwvutsrqponmlkjihgfedcba', 4)),
                                 ''.join(random.sample('zyxwvutsrqponmlkjihgfedcba', 4)),
                                 str(float(time.time())))

    @classmethod
    def generate_phone(self):
        prefix = [
            '130', '131', '132', '133', '134', '135', '136', '137', '138', '139',
            '145', '147', '149', '150', '151', '152', '153', '155', '156', '157',
            '158', '159', '165', '171', '172', '173', '174', '175', '176', '177',
            '178', '180', '181', '182', '183', '184', '185', '186', '187', '188',
            '189', '191'
        ]

        # 随机取一个手机号前缀
        pos = random.randint(0, len(prefix) - 1)
        # 随机生成后8位数字
        suffix = str(int(time.time() * 1000))[-8:]
        # 拼接返回11位手机号
        return prefix[pos] + suffix

    @classmethod
    def current_subtle_unix(self):
        # 当前微妙时间
        return int(time.time() * 1000)

    def generate_email(self, domain='163.com'):
        """
        获取一个随机邮箱号
        :param domain:域名，默认163邮箱
        :return:
        """
        random_str = ''.join(random.sample('zyxwvutsrqponmlkjihgfedcba0123456789', random.randint(6, 20)))
        return 'test_{}@{}'.format(random_str, domain)

    @property
    def current_unix(self):
        # 当前时间
        return int(time.time())

    @property
    def current_subtle_unix_str(self):
        # 当前微妙时间
        # 等待1微妙防止重复
        time.sleep(0.001)
        return str(int(float(time.time()) * 100000))

    @property
    def current_subtle_str_unix(self):
        # 当前微妙时间（字符串类型）
        # 等待1微妙防止重复
        time.sleep(0.001)
        return str(int(float(time.time()) * 1000))

    def get_age_unix(self, num, is_positive=False):
        '''
            获取一个年龄超过n岁的时间
            is_positive 为false，取当前时间往前n年的时间
            is_positive 为true，取当前时间往后n年的时间
        '''
        num = int(num)
        _format = "%Y-%m-%d"
        today = datetime.date.today().strftime(_format)
        current_date = today.split()[0]
        y = current_date.split('-')[0]
        if is_positive is False:
            age = '{}-{}'.format(str(int(y) - num), '-'.join(current_date.split('-')[1:]))
        else:
            age = '{}-{}'.format(str(int(y) + num), '-'.join(current_date.split('-')[1:]))
        self.logger.debug(age)
        return int(time.mktime(time.strptime(age, _format)))

    @property
    def yesterday_start_unix(self):
        # 昨天开始时间
        return self.get_start_unix(1)

    def get_start_unix(self, day):
        '''
        获取n天前的开始时间
        @param day: n，提前n天
        @return:unix时间戳
        '''
        return int(
            time.mktime(time.strptime(str(datetime.date.today() - datetime.timedelta(days=int(day))), '%Y-%m-%d')))

    def get_start_date(self, day, format='%Y-%m-%d %H:%M:%S'):
        '''
        获取n天前的开始时间
        @param day: n，提前n天
        @param format: 时间格式
        @return:字符串时间
        '''
        return self.strp_unix_by_date(self.get_start_unix(day), format)

    def get_end_unix(self, day):
        '''
        获取n天前的结束时间
        @param day: n，提前n天
        @return:unix时间戳
        '''
        return self.get_start_unix(int(day) - 1) - 1

    def get_end_date(self, day, format='%Y-%m-%d %H:%M:%S'):
        '''
        获取n天前的结束时间
        @param day: n，提前n天
        @param format: 时间格式
        @return:字符串时间
        '''
        return self.strp_unix_by_date(self.get_end_unix(day), format)

    @property
    def yesterday_end_unix(self):
        # 昨天结束时间
        return int(time.mktime(time.strptime(str(datetime.date.today()), '%Y-%m-%d'))) - 1

    @property
    def today_start_unix(self):
        # 今天开始时间
        return int(time.mktime(time.strptime(str(datetime.date.today()), '%Y-%m-%d')))

    @property
    def today_end_unix(self):
        # 今天结束时间
        return int(time.mktime(time.strptime(str(datetime.date.today() + datetime.timedelta(days=1)), '%Y-%m-%d'))) - 1

    @property
    def tomorrow_start_unix(self):
        # 明天开始时间戳
        return int(time.mktime(time.strptime(str(datetime.date.today() + datetime.timedelta(days=1)), '%Y-%m-%d')))

    @property
    def tomorrow_end_unix(self):
        # 明天结束时间
        return int(time.mktime(time.strptime(str(datetime.date.today() + datetime.timedelta(days=2)), '%Y-%m-%d'))) - 1

    def strp_date_by_unix(self, date, format='%Y-%m-%d'):
        '''
        将字符串时间或datetime时间转换为unix时间
        @param date:字符串时间
        @param format:字符串时间格式，默认%Y-%m-%d,其他参考值%Y-%m-%d %H:%M:%S.%f
        @return:
        '''
        if type(date) == str:
            date = datetime.datetime.strptime(date, format)
        if format == '%Y-%m-%d %H:%M:%S.%f':
            return time.mktime(date.timetuple()) * 1e3 + date.microsecond / 1e3
        return time.mktime(date.timetuple())

    def current_local_date_str(self, format='%Y-%m-%d %H:%M:%S'):
        '''
        获取当前时间
        @param format: 返回格式，默认%Y-%m-%d %H:%M:%S
        @return:
        '''
        return datetime.datetime.now().strftime(format)

    def strp_unix_by_date(self, date, format='%Y-%m-%d %H:%M:%S'):
        '''
        将unix时间转换为字符串时间
        @param date:unix时间
        @param format:字符串时间格式，默认%Y-%m-%d,其他参考值%Y-%m-%d %H:%M:%S
        @return:
        '''
        # value为传入的值为时间戳(整形)，如：1332888820
        value = time.localtime(date)
        return time.strftime(format, value)

    def _sum(self, *args):
        '''
        求和，此函数解决float相加或相减
        @param args:
        @return:
        '''
        total = 0
        for i in args:
            total = Decimal(str(float(total))) + Decimal(str(float(i)))
        return float(total)

    def get_unique_identification(self):
        """
        获取唯一标识，多线程可用，用于性能测试使用
        """
        return 'test{}_{}_{}'.format(''.join(random.sample('zyxwvutsrqponmlkjihgfedcba', 4)),
                                              ''.join(random.sample('zyxwvutsrqponmlkjihgfedcba', 4)),
                                              str(float(time.time())))
