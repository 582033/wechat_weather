#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import os
import requests
from bs4 import BeautifulSoup
from threading import Thread


def get_all_url():
    host = 'http://tianqi.2345.com'

    sheng_list = requests.get('http://tianqi.2345.com').content

    sheng_soup = BeautifulSoup(sheng_list)
    div_sheng = sheng_soup.findAll('div', {'class':'bmeta'})[1].findAll('div', {'class':'clearfix'})[0]

    all_url = []
    for a in div_sheng:
        all_url.append(a['href'])
    return all_url

def get_city(url):
    city_list = requests.get(url).content
    city_soup = BeautifulSoup(city_list)

    dd_city = city_soup.findAll('dd')
    dd_city.pop()

    for dd in dd_city:
        a_list = dd.findAll('a')
        for a in a_list:
            href = a['href']
            city_name = a.string
            city_pinyin = re.findall(r'\w+', href)[0]
            city_code = re.findall(r'\d+', href)[0]
            string =  u"'%s': {'code':%s, 'name':u'%s'},\n" % (city_pinyin, city_code, city_name)
            f = open('city.txt', 'a')
            f.write(string.encode('utf-8'))
            f.close()

if __name__ == "__main__":
    all_url = get_all_url()
    for url in all_url:
        Thread(target = get_city, args = [url]).start()

#cat city.txt | sort -n > city_code.txt
