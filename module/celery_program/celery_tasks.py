# -*- coding: utf-8 -*-
from api.celery_app import celery_app
from module.background.background_service import BackgroundService
from utils.log import LOG


@celery_app.task(name="period_hw_test")
def celery_hello_world():
    """
    hello world 测试

    :return:
    """
    print "celery status check"
    # LOG.info("celery status check")
    return 'hello world'


@celery_app.task(name="period_run_crawler")
def celery_period_run_crawler():
    """
    Run web crawler to get new articles
    :return:
    """
    bgs = BackgroundService(mode="update")
    bgs.run_wechat_crawler()

    return "Done"


if __name__ == '__main__':
    celery_period_run_crawler.delay()





