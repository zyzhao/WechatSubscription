# -*- coding: utf-8 -*-
import config.config as config
from celery.schedules import crontab
from module.celery_program.celery_tasks_name import *
from kombu import Exchange, Queue

BROKER_URL = 'amqp://%s:%s@%s:%s/%s' % (config.RMQ_BROKER_USER,
                                        config.RMQ_BROKER_PASS,
                                        config.RMQ_BROKER_IP,
                                        config.RMQ_BROKER_PORT,
                                        config.RMQ_BROKER_VHOST)

# CELERY_RESULT_BACKEND = 'mongodb://%s:%s/%s' % (config.SUBS_NOTIF_ORG_IP,
#                                                 config.SUBS_NOTIF_ORG_PORT,
#                                                 config.SUBS_NOTIF_ORG_COLLECTION)

CELERY_QUEUE_HA_POLICY = 'all'
CELERY_ACKS_LATE = True
CELERY_RESULT_PERSISTENT = True
CELERYD_PREFETCH_MULTIPLIER = 1

CELERYD_CONCURRENCY = 4
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']

CELERY_TIMEZONE = 'Asia/Shanghai'
CELERY_ENABLE_UTC = True

CELERYBEAT_SCHEDULE = {
    'periodic_auto_hw_task': {
        'task': 'period_hw_test',
        'schedule': crontab()
    },
    "period_auto_run_crawler": {
        'task': 'period_run_crawler',
        'schedule': crontab(hour='0,6,12,18', minute=0),
    }
}


#
# CELERY_QUEUES = (
#     Queue('wechat_task', Exchange('wechat_task'), routing_key='wechat_task'),
# )
#
# CELERY_ROUTES = {
#     "period_hw_test": {'queue': 'wechat_task', 'routing_key': 'wechat_task'},
# }