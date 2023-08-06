#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
from elasticsearch import Elasticsearch, helpers

from logger.total_logger import TotalLogger


class EsTotalLogger(TotalLogger):

    def __init__(self, host, port, index='', **kwargs):

        # 核心路由参数
        self.host = host
        self.port = port
        self.index = index


    def log(self, id, remark, **kwargs):
        now = datetime.datetime.now().strftime("%Y%m%d")
        index_name = '%s_%s' % (self.index, now)

        log = {
            'id':id,
            'create_date': datetime.datetime.now().isoformat(),
            'remark': remark
        }

        for key, item in kwargs.items():
            log[key] = item

        action = {'_op_type': 'index',
                  '_id': id,
                  '_index': index_name,
                  '_source': log}

        es = Elasticsearch(hosts=self.host, port=self.port)
        helpers.bulk(client=es, actions=[action])



