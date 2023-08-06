# Press the green button in the gutter to run the script.
import traceback

import pytest

from logger.logger_factory import LoggerFactory


class TestTotalLogger:

    def setup(self):
        self.config = {
            "host": "192.168.4.47",
            "port": "29200",
            "index": "spider_total_log_email_classify"
        }

    def teardown(self):
        print('关闭客户端')


    def test_log(self):
        """
        测试写统计日志
        """
        logger = LoggerFactory.get_total_logger(self.config)
        logger.log('11111111111','test',type='business')


if __name__ == '__main__':
    pytest.main(["-q"])
