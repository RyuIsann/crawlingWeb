'''
This Python code is for getting data from SZSE webpage and save those data in a csv file.
'''

from urllib import request
from selenium import webdriver
import requests
import re
import time
import csv
import codecs

class SZData:

    def __init__(self, url):
        self.url = url


    def get_person_list(self, begin_page, end_page):

        browser = webdriver.Chrome()
        browser.maximize_window()
        browser.get(self.url)
        time.sleep(2)
        data_person = []


        browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        browser.find_elements_by_id("1801_cxda_tab1_naviboxid")[0].clear()
        browser.find_elements_by_id("1801_cxda_tab1_naviboxid")[0].send_keys(begin_page)
        browser.find_elements_by_name("navigatebutton")[2].click()


        for i in range(0, end_page - begin_page + 1):

            time.sleep(3)
            pattern_table = re.compile('变动人与董监高的关系</th></tr>(.*?)</table>')
            data_table = re.findall(pattern_table, browser.page_source)
            pattern_person = re.compile('<td width="60" align="center">(.*?)</tr>')
            data_person = data_person + re.findall(pattern_person, data_table[0])
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            browser.find_elements_by_name("navigatebutton")[1].click()

        browser.close()

        pattern_information = re.compile('(.*?)</td>')
        pattern_personal_information1 = re.compile('"center">(.*?)$')
        pattern_personal_information2 = re.compile('"right">(.*?)$')
        persons = []

        for person in data_person:
            stock_holder = {}
            """get the stock id"""

            information = re.findall(pattern_information, person)

            stock_holder["1. 证券代码"] = information[0]
            stock_holder["2. 证券简称"] = re.findall(pattern_personal_information1, information[1])[0]
            stock_holder["3. 董监高姓名"] = re.findall(pattern_personal_information1, information[2])[0]
            stock_holder["4. 变动日期"] = re.findall(pattern_personal_information1, information[3])[0]
            stock_holder["5. 变动股份数量"] = re.findall(pattern_personal_information2, information[4])[0]
            stock_holder["6. 成交均价"] = re.findall(pattern_personal_information2, information[5])[0]
            stock_holder["7. 变动原因"] = re.findall(pattern_personal_information1, information[6])[0]
            stock_holder["8. 变动比例"] = re.findall(pattern_personal_information1, information[7])[0]
            stock_holder["9. 当日结存股数"] = re.findall(pattern_personal_information1, information[8])[0]
            stock_holder["10. 股份变动人姓名"] = re.findall(pattern_personal_information1, information[9])[0]
            stock_holder["11. 职务"] = re.findall(pattern_personal_information1, information[10])[0]
            stock_holder["12. 变动人和董监高的关系"] = re.findall(pattern_personal_information1, information[11])[0]

            #print(stock_holder)

            persons.append(stock_holder)


        return persons


szData = SZData("http://www.szse.cn/main/disclosure/jgxxgk/djggfbd/")
szDataList = szData.get_person_list(440, 690)
print(szDataList)

with codecs.open('/Users/ryu_isann/Desktop/szdata.csv', 'w','gbk') as csvFile:
    writer = csv.writer(csvFile)
    writer.writerow(
        ["证券代码", "证券简称", "董监高姓名", "变动日期", "变动股份数量", "成交均价", "变动原因", "变动比例", "当日结存股数", "股份变动人姓名", "职务", "变动人和董监高的关系"])
    for item in szDataList:
        row = []
        for key in item:
            row.append(item[key])
        writer.writerow(row)
    csvFile.close()





