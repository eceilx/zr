# -*- coding: UTF-8
# 职位来

import gevent
from gevent import monkey
gevent.monkey.patch_all()
import json
import time
import config
from func import BaseRequest
from func import User


today = time.strftime('%Y-%m-%d', time.localtime())

def time_url_encode(time):
    return (time+":00").replace(':', '%3A')

def checkin(u):
    if not u['enableAutoCheckin']:
        return
    usr = User(u['xuehao'], u['password'], cfg['school_id'])
    usr.login()
    x = usr.get_current_reservation()
    for rsv in x['list']:
        if today in rsv['timeDay']:
            usr.scan_to_sit(rsv['seatId'])
            print(usr.name,rsv['seatNum'],'已签到')
    



if __name__ == "__main__":
    global cfg
    with open("config.json") as f:
        cfg = json.load(f)
    # print(cfg)

    gevent.joinall([gevent.spawn(checkin, u) for u in cfg['users']])

