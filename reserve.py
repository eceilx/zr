# -*- coding: UTF-8
# 职位来
import gevent
from gevent import monkey
gevent.monkey.patch_all()

import datetime
from func import *

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
    cfg = load_cfg()

    gevent.joinall([gevent.spawn(reserve, u) for u in cfg['users']])
