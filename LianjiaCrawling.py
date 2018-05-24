'''
This code is for getting Lianjia Website data from its webpage.
By using regex, we can catch the prices of houses in each district of Beijing, and
save these data in a csv file. 
'''

import re
import urllib
import os
from os import path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from numpy import zeros
from pandas import DataFrame
import ssl
import csv
import codecs


class Houses():
    def __init__(self, url):
        self.url = url

    def data(self, page_index, local):
        url = "https://bj.lianjia.com/ershoufang/" + local + "/pg" + str(page_index) + "/"
        request = urllib.request.urlopen(url, context = ssl._create_unverified_context())
        imform0 = request.read().decode('utf-8')
        return imform0

    def house_information(self, page, local):
        imform0 = self.data(page, local)
        pattern_title = re.compile(
            'data-sl="">(.*?)</span></div></div></div><div class="listButtonContainer"><div class="btn-follow followBtn"')
        houses = re.findall(pattern_title, imform0)
        names = []
        for house in houses:
            item = {}

            pattern_title = re.compile('alt="(.*?)"></a><div class="info clear"><div class="title">')
            title = re.findall(pattern_title, house) + ['']
            item['title'] = title[0]

            pattern_location = re.compile('data-el="region">(.*?)</a><span class="divide">')
            location = re.findall(pattern_location, house) + ['']
            item['location'] = location[0]

            pattern_information = re.compile('</span>(.*?)<span class="divide">')
            informations = re.findall(pattern_information, house) + ['']
            item['space'] = ''
            for information in informations:
                if '平米' in information:
                    item['space'] = information

            pattern_subway = re.compile('<span class="subway">(.*?)</span>')
            subway = re.findall(pattern_subway, house) + ['']
            item['distance to subway'] = subway[0]

            pattern_taxfree = re.compile('<span class="taxfree">(.*?)</span>')
            taxfree = re.findall(pattern_taxfree, house)
            if taxfree:
                item['taxfree'] = taxfree[0]
            else:
                pattern_taxfree1 = re.compile('<span class="five">(.*?)</span>')
                taxfree = re.findall(pattern_taxfree1, house) + ['']
                item['taxfree'] = taxfree[0]

            pattern_price = re.compile('data-price="(.*?)"><span>')
            price = re.findall(pattern_price, house) + ['']
            item['price'] = price[0]

            names.append(item)

        return names

    def house_data(self, page, local):
        imform0 = self.data(page, local)
        pattern_title = re.compile(
            'data-sl="">(.*?)</span></div></div></div><div class="listButtonContainer"><div class="btn-follow followBtn"')
        houses = re.findall(pattern_title, imform0)
        names = []
        for house in houses:
            item = []

            pattern_information = re.compile('</span>(.*?)<span class="divide">')
            informations = re.findall(pattern_information, house) + ['']
            for information in informations:
                if '平米' in information:
                    information0 = information
            pattern_space = re.compile('(.*?)平米')
            space = re.findall(pattern_space, information0)

            pattern_price = re.compile('data-price="(.*?)"><span>')
            price = re.findall(pattern_price, house)

            if space and price:
                item = [float(space[0]), int(price[0])]
                names.append(item)
        return names

    def get_number_of_page(self, local):
        inform0 = self.data(1, local)

        pattern_page_number = re.compile('"totalPage":(.*?),"curPage')
        page_number = re.findall(pattern_page_number, inform0)

        return int(page_number[0])



houses = Houses("https://bj.lianjia.com/ershoufang/")
houselist = ""
city_list = ['tongzhou', 'haidian', 'pinggu']
page_list = [4, 5, 1]

for i in range(0, 3):
    
    HouseList = []
    print("house data of " + city_list[i] + " are as follows:")
    pagenumber = houses.get_number_of_page(city_list[i])
    for pages in range(1, pagenumber):
        HouseList = HouseList + houses.house_information(pages, 'tongzhou')
    rank = 1

    for house in HouseList:
        print(rank)
        print("标题：    " + house['title'])
        print("地理位置：" + house['location'])
        print("房源面积：" + house['space'])
        if house['distance to subway'] != '':
            print("地铁站：  " + house['distance to subway'])
        if house['taxfree'] != '':
            print("房产证：  " + house['taxfree'])
        print("均价：    " + house['price'] + "/平米")
        houselist = houselist + house['title'] + " "
        print("")
        rank = rank + 1

    with codecs.open('/Users/ryu_isann/Desktop/' + city_list[i] +'.csv', 'w', 'gbk') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(['标题', '位置', '面积', '地铁站距离', '房产证情况', '单价（每平米）'])
        for item in HouseList:
            row = []
            for key in item:
                row.append(item[key])
            writer.writerow(row)
        csvFile.close()
