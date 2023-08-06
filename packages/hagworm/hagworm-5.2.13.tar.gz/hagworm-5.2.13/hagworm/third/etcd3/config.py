# -*- coding: utf-8 -*-

__author__ = r'wsb310@gmail.com'

from etcd3gw.client import Etcd3Client

from ...extend.config import ConfigureBase


class Etcd3Configure(ConfigureBase):
    """基于etcd3的配置类
    """

    __slots__ = [r'_client', r'_key_prefix', r'_watch_prefix']

    def __init__(self, host, port=2379, *, key_prefix, api_path=r'/v3/', **kwargs):

        super().__init__()

        self._client = Etcd3Client(host, port, **kwargs, api_path=api_path)

        self._key_prefix = key_prefix

        self._watch_prefix = self._client.watch_prefix(self._key_prefix)

    def for_watch(self):

        temp = self._watch_prefix[0]

        for _item in self._watch_prefix[0]:
            print(_item)

    def load(self):

        setting = {}

        _resp = self._client.get_prefix(self._key_prefix)

        for _item in _resp:

            _key = _item[1][r'key'].decode()

            if _key.find(self._key_prefix) == 0:
                _key = _key.replace(self._key_prefix, r'', 1)

            setting[_key] = _item[0].decode()

        for _key, _field in self.__dataclass_fields__.items():

            _type = _field.type
            _section = _field.default.section

            if _type in (str, int, float, bool):
                self.__setattr__(_key, _type(setting[f'{_section}/{_key}']))
            else:
                self.__setattr__(_key, _type.decode(setting[f'{_section}/{_key}']))
