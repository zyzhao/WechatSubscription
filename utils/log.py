# -*- coding: utf-8 -*-
import logging

"""
输出标准化:
[时间 level]: [文件名.函数名]
"""
logging.basicConfig(level=logging.DEBUG,
                    format='[%(asctime)s %(levelname)s]: [%(module)s.%(funcName)s()]: %(message)s')

# requests函数LOG, 只有warning以上级别打印log
logging.getLogger("requests").setLevel(logging.WARNING)

LOG = logging.getLogger()


if __name__ == "__main__":
    LOG.info("HELLO WORLD")
    LOG.debug("HELLO WORLD")
    LOG.error("error")








