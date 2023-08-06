#!/usr/bin/env python
# -*- coding: utf-8 -*-
from logger.es_logger import EsLogger
from logger.es_total_logger import EsTotalLogger


class LoggerFactory:

    @staticmethod
    def get_logger(config, **kwargs):
        return EsLogger(config['host'], config['port'], config['index'],**kwargs)

    @staticmethod
    def get_total_logger(config, **kwargs):
        return EsTotalLogger(config['host'], config['port'], config['index'], **kwargs)

