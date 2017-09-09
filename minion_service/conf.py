# coding:utf-8
import yaml
import os
import sys


class BaseConfig(dict):
    def __getitem__(self, items):
        items = items.split('.')
        temp = self.copy()
        for item in items:
            temp = temp[item]
        if isinstance(temp, dict):
            return BaseConfig(**temp)
        else:
            return temp

    def __setitem__(self, key, value):
        self[key] = value

    def __getattr__(self, item):
        try:
            return self[item]
        except:
            if item == 'path':
                return ''
            raise

    def get(self, k, d=None):
        try:
            return self[k]
        except:
            return d


class Config(BaseConfig):
    __instance = None

    def __init__(self, config_file=None, **kwargs):
        super(Config, self).__init__(**kwargs)
        BASEDIR = os.path.abspath(os.path.dirname(__file__))
        if not config_file:
            self._default_config()
            self.file_path = self.default_file
        else:
            self.file_path = config_file
        self._load_config(self.file_path)
        self.base_dir = BASEDIR

    def _default_config(self):
        if sys.platform.startswith('win'):
            self.default_file = 'D:/scrapy_workstation/minion_config.yaml'
            self.log_file = 'D:/scrapy_workstation/log/minion_service.log'
        else:
            self.default_file = '/root/project/scrapy_workstation/minion_config.yaml'
            self.log_file = '/root/project/scrapy_workstation/log/minion_service.log'

    def _load_config(self, file_path):
        config = yaml.load(open(file_path))
        self.update(config)

    def __new__(cls, *args, **kwargs):  # 单例模式
        if Config.__instance is None:
            Config.__instance = dict.__new__(cls, *args, **kwargs)
        return Config.__instance
