# -*- coding: UTF-8
# 职位来
import gevent
from gevent import monkey
gevent.monkey.patch_all()
import datetime
import time
from func import User
from func import BaseRequest
import config
import json



def time_url_encode(time):
    return (time+":00").replace(':', '%3A')


tomorrow = datetime.date.today()+datetime.timedelta(1)


def reserve(u):
    if not u['enableAutoReserve']:
        return
    usr = User(u['xuehao'], u['password'], cfg['school_id'])
    usr.login()
    t = str(tomorrow)
    start = t + '+' + time_url_encode(u['time_start'])
    end = t + '+' + time_url_encode(u['time_end'])
    # print(start, end)
    res = usr.reserve(u['seat_id'], start, end)
    if res['success']:
        print('✓', usr.name.ljust(5), '预约成功')
    else:
        print('✗', usr.name.ljust(5), res['message'])


if __name__ == "__main__":
    global cfg
    with open("/home/elx/PY/zr/config.json") as f:
        cfg = json.load(f)
    print(cfg)

    gevent.joinall([gevent.spawn(reserve, u) for u in cfg['users']])
