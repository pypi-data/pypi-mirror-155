#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
from elasticsearch import Elasticsearch, helpers

from logger.logger import Logger


class EsLogger(Logger):

    def __init__(self, host, port, index='spider_log_container', **kwargs):

        # 核心路由参数
        self.host = host
        self.port = port
        self.index = index
        self.is_batch = kwargs['is_batch'] if 'is_batch' in kwargs else False

        # 非核心参数
        self.__logs = []

    def begin(self):
        self.__logs = []

    def commit(self):
        self._push_es(self.__logs)
        self.__logs = []

    def error(self, message, ex, **kwargs):
        self._log('ERROR', message, ex, **kwargs)

    def warn(self, message, **kwargs):
        self._log('WARN', message, **kwargs)

    def info(self, message, **kwargs):
        self._log('INFO', message, **kwargs)

    def debug(self, message, **kwargs):
        self._log('DEBUG', message, **kwargs)

    def _log(self, level, message, ex=None, **args):
        now = datetime.datetime.now().isoformat()
        log = {
            '@timestamp':datetime.datetime.now().isoformat(),
            'level': level,
            'create_time': now,
            'message': message,
            'error': ex
        }
        for key, item in args.items():
            log[key] = item

        if self.is_batch:
            self.__logs.append(log)
        else:
            self._push_es([log])

    def _push_es(self, logs):
        index_name = '%s_%s' % (self.index, datetime.datetime.now().strftime("%Y%m%d"))
        actions = []
        for lg in logs:
            action = {'_op_type': 'index',
                      '_index': index_name,
                      '_source': lg}
            actions.append(action)

        es = Elasticsearch(hosts=self.host, port=self.port)
        helpers.bulk(client=es, actions=actions)
