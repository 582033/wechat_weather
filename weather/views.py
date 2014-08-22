# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext, Template
from django.utils.encoding import smart_str, smart_unicode
import hashlib
from xml.etree import ElementTree as etree
from weather import weather
import re
from keyword_dict import joke
import pinyin
from turing_robot import turing

@csrf_exempt
def weixin(request):
    if request.method=='GET':
        response=HttpResponse(checkSignature(request))
        return response
    else:
        xmlstr = smart_str(request.body)
        xml = etree.fromstring(xmlstr)

        ToUserName = xml.find('ToUserName').text
        FromUserName = xml.find('FromUserName').text
        CreateTime = xml.find('CreateTime').text
        MsgType = xml.find('MsgType').text
        Content = xml.find('Content').text
        MsgId = xml.find('MsgId').text
        reply_xml = """<xml>
        <ToUserName><![CDATA[%s]]></ToUserName>
        <FromUserName><![CDATA[%s]]></FromUserName>
        <CreateTime>%s</CreateTime>
        <MsgType><![CDATA[text]]></MsgType>
        <Content><![CDATA[%s]]></Content>
        </xml>"""%(FromUserName,ToUserName,CreateTime,reply(Content))
        return HttpResponse(reply_xml)

def reply(msg):
    #msg = 'beijing'
    wt = weather()
    pymsg = pinyin.get(msg)
    if wt.city_code.has_key(pymsg):
        result = wt.get_weather(pymsg)
    else:
        result = "你在说什么?我只支持天气查询哦.\n\n试着输入要查询的地区吧,比如'北京'"
        joke_num = False
        for key in joke:
            reg = re.search(key, pymsg)
            if reg:
                result = joke[reg.group(0)]
                joke_num = True
        if not joke_num:
            robot = turing()
            result = robot.reply(msg)
    return result

def checkSignature(request):
    signature=request.GET.get('signature',None)
    timestamp=request.GET.get('timestamp',None)
    nonce=request.GET.get('nonce',None)
    echostr=request.GET.get('echostr',None)
    #这里的token我放在setting，可以根据自己需求修改
    token="yjiang"

    tmplist=[token,timestamp,nonce]
    tmplist.sort()
    tmpstr="%s%s%s"%tuple(tmplist)
    tmpstr=hashlib.sha1(tmpstr).hexdigest()
    if tmpstr==signature:
        return echostr
    else:
        return "<a href='http://yjiang.tk'>http://yjiang.tk</a>"
