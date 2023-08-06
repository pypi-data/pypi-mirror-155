# Press the green button in the gutter to run the script.
import traceback

import pytest

from logger.logger_factory import LoggerFactory


class TestLogger:

    def setup(self):
        self.config = {
            "host": "192.168.4.47",
            "port": "29200",
            "index": "spider_log_container_tracking"
        }

    def teardown(self):
        print('关闭客户端')

    def test_error(self):
        """
        测试立即记录错误日志
        """
        logger = LoggerFactory.get_logger(self.config, is_batch=False)
        try:
            1 / 0
        except ZeroDivisionError as ex:
            logger.error('ES落库异常，原因:网络异常', traceback.format_exc(), trace_id='11')

    def test_info(self):
        """
        测试立即写信息日志
        """
        logger = LoggerFactory.get_logger(self.config, is_batch=False)
        logger.info('ES落库成功')

    def test_batch(self):
        """
        测试批量提交
        """
        logger = LoggerFactory.get_logger(self.config, is_batch=True)
        try:
            1 / 0
        except ZeroDivisionError as ex:
            logger.error('ES落库异常，原因:网络异常', traceback.format_exc(), trace_id='11')

        logger.info('测试落库成功',trace_id='123')
        logger.commit()


if __name__ == '__main__':
    pytest.main("-q --html=report.html")
