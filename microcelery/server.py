# coding: utf-8

import re
import json
import time
import redis
import argparse
import importlib
import multiprocessing

import settings


class Server(object):

    def __init__(self, app):
        self.rds = redis.Redis()
        self.app = app

    def _execute_task(self, raw_task):
        funcname, args, kwargs = json.loads(raw_task)
        func = self.app._tasks[funcname]
        proc = multiprocessing.Process(target=func, args=args, kwargs=kwargs)
        proc.start()

    def _listen_queue(self):
        while True:
            raw_task = self.rds.lpop(settings.QUEUE_KEY)
            if raw_task:
                self._execute_task(raw_task)
            else:
                break

    def run(self):
        while True:
            self._listen_queue()
            time.sleep(0.5)


def import_app(app_path):
    module_path, app_name = re.match(r"(.*)\.(.*)", app_path).groups()
    module = importlib.import_module(module_path)
    return getattr(module, app_name)


def get_args():
    parser = argparse.ArgumentParser(
        description="Microwave, microsoft, microcelery, stuffs like that")
    parser.add_argument("-A", "--app-path", required=True, help="Application path")
    return parser.parse_args()


if __name__ == '__main__':
    args = get_args()
    app = import_app(args.app_path)
    server = Server(app)
    server.run()
