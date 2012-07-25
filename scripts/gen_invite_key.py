#!/usr/bin/env python
#coding=utf=8
import config

import tornado.options
tornado.options.parse_command_line()

#models/base.py会初始化数据库，所以传入的命令行参数需在此之前
import models
from utils import gen_invite_key
import sys


def run():
    hash = gen_invite_key()
    models.Invite_Key(
            user_id = 0,
            hash = hash,
            ).save()
    print '/register?invite_key=%s'%hash

if __name__ == '__main__':
    run()

