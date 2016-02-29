# -*- coding: utf-8 -*-
from api.celery_app import celery_app
from module.celery_program.celery_tasks import celery_hello_world

if __name__ == '__main__':
    celery_hello_world.delay()

