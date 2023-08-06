import os
import sys
from itertools import chain

from setuptools import setup, find_packages


def generate_data_files():
    data_files = []
    data_dirs = (r'src\autoTestScheme\allure',)
    for path, dirs, files in chain.from_iterable(os.walk(data_dir) for data_dir in data_dirs):
        install_dir = os.path.join(sys.prefix, path)
        list_entry = (install_dir, [os.path.join(path, f) for f in files if not f.startswith('.')])
        data_files.append(list_entry)
        print(list_entry)
    return data_files


install_requires = [
    "locust",
    "redis-py-cluster",
    'pluggy==0.13.1',
    "loguru",
    "dingtalkchatbot",
    "allure-pytest",
    "pytest-ordering",
    "pymysql",
    "json_tools",
    "pytest~=6.2.5",
    "pako~=0.3.1",
    "websocket-client",
    "Faker",
    "pycryptodome",
    "dynaconf",
    "selenium",
    "webdriver_manager",
]

packages = find_packages("src")

long_description = "1.json数据字段校验"


setup(name='autoTestScheme',
      version='0.2.0.23',
      url='https://gitee.com/xiongrun/auto-test-scheme',
      author='wuxin',
      description='auto test scheme',
      long_description=long_description,
      long_description_content_type='text/markdown',
      author_email='xr18668178362@163.com',
      install_requires=install_requires,
      project_urls={'Bug Tracker': 'https://gitee.com/xiongrun/auto-test-scheme/issues'},
      package_dir={'': 'src'},
      packages=packages,
      include_package_data=True,
      entry_points={'pytest11': ['pytest_autoTestScheme = autoTestScheme']},
      data_files=generate_data_files(),
      package_data={
          'demo': ['demo/*'],
          'autoTestScheme': ['allure'],
      },
      )
