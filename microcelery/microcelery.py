# coding: utf8

from redis import Redis

import settings
from task import Task


class MicroCelery(object):

    def __init__(self):
        self._tasks = {}
        self.rds = Redis()

    def task(self, func):
        task = Task(self, func)
        self._tasks[func.__name__] = task
        return task

    def add_task(self, data):
        self.rds.rpush(settings.QUEUE_KEY, data)

