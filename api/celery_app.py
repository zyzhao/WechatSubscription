# -*- coding: utf-8 -*-
from celery import Celery

celery_app = Celery(include=["module.celery_program.celery_tasks"])
celery_app.config_from_object("module.celery_program.celery_config")

if __name__ == '__main__':
    celery_app.start()