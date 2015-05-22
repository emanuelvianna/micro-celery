# coding: utf8

import json


class Task(object):
    
    def __init__(self, app, func):
        self.app = app
        self.func = func

    def __call__(self, *args, **kwargs):
        result = self.func(*args, **kwargs)

    def delay(self, *args, **kwargs):
        dump = json.dumps((self.func.__name__, args, kwargs))
        self.app.add_task(dump)

