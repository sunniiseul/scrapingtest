import time
from datetime import date, timedelta
import re
import csv
import openpyxl
from selenium import webdriver
import urllib
import requests
from bs4 import BeautifulSoup

datelist = []

raw_date = date.today()
for i in range(0,7):
    date_input = str(raw_date.year) + str(raw_date.strftime("%m")) + str(raw_date.strftime("%d"))
    datelist.append(date_input)
    raw_date = raw_date + timedelta(days=1)
    i = i + 1

f = open('schedule.csv', 'w', encoding='utf-8')

driver = webdriver.Chrome("./chromedriver")

url = "https://www.gsshop.com/shop/tv/tvScheduleMain.gs?lseq=415680-1&gsid=ECmain-AU415680-AU415680-1#{}_LIVE"
#driver.get("https://www.gsshop.com/shop/tv/tvScheduleMain.gs?lseq=415680-1&gsid=ECmain-AU415680-AU415680-1#{}_LIVE")

for i in datelist:
    link = url.format(i)
    print(link)
    driver.get(link)
    #driver.implicitly_wait(2)
    time.sleep(3)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    timeslots = soup.select("article.items")
    for tslot in timeslots:
        live_time = tslot.select_one("span.times").text.strip()
        productslots = tslot.select("li.prd-item")
        for prdslot in productslots:
            product = prdslot.select_one("dt.prd-name").text.strip()
            """
            prd_names = str(product)
            prd_names = re.sub(pattern='[TV상품]', repl='', string=prd_names)
            prd_names = re.sub(pattern='[]', repl='', string=prd_names)
            product = prd_names.strip()
            """
            #prd_names = re.sub('^{30}', '', prd_names, 0).strip()
            f.write(i+","+live_time+","+product+"\n")
            #print(live_time, product)

f.close()
