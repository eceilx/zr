# -*- coding: UTF-8
# 职位来
import gevent
from gevent import monkey
gevent.monkey.patch_all()

from func import *
import time


today = time.strftime('%Y-%m-%d', time.localtime())

def checkin(u):
    if not u['enableAutoCheckin']:
        return
    usr = User(u['xuehao'], u['password'], cfg['school_id'])
    usr.login()
    x = usr.get_current_reservation()
    if not x:
        print('⊙', usr.name, '此人没有预约')
        return
    isAnyCheckIn = False
    for rsv in x['list']:
        if today in rsv['timeDay']:
            usr.scan_to_sit(rsv['seatId'])
            isAnyCheckIn = True
            print('✓', usr.name, rsv['seatNum'], '已签到')
    if not isAnyCheckIn:
        print('✗', usr.name, '今天没有预约')

if __name__ == "__main__":
    global cfg
    cfg = load_cfg()

    gevent.joinall([gevent.spawn(checkin, u) for u in cfg['users']])
