#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import json

class turing():
    def __init__(self):
        self.host = 'http://www.tuling123.com'
        self.key = '5de60197e6bb2eb33029f3468e5b145c'
        self.api = '%s/openapi/api?key=%s&info=' % (self.host, self.key)

    def reply(self, msg):
        request_url = self.api + msg
        result = requests.get(request_url).content
        obj = json.loads(result)
        if obj['code'] == 100000:
            return obj['text']
        else:
            return u"你在说什么?我只支持天气查询哦.\n\n试着输入要查询的地区吧,比如'北京'"

if __name__ == '__main__':
    robot = turing()
    print robot.reply(u'傻逼')
