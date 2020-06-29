#google sheet dev version
# -*- coding: utf-8 -*-

import gspread
from oauth2client.service_account import ServiceAccountCredentials

##Sheet###############################
#내가 사용할 google api
scope = [
'https://spreadsheets.google.com/feeds',
'https://www.googleapis.com/auth/drive',
]

#파이썬과 같은 경로에 복사 from 구글api

json_file_name = 'analog-hull-281314-3e3305abac8a.json'

credentials = ServiceAccountCredentials.from_json_keyfile_name(json_file_name, scope)
gc = gspread.authorize(credentials)

spreadsheet_url = 'https://docs.google.com/spreadsheets/d/1vVeVtex3yVkZBFLz6SAbN19Ioyh5mCvV2CghHVxHXcg/edit#gid=0'

# 스프레스시트 문서 가져오기 
doc = gc.open_by_url(spreadsheet_url)

# 시트 선택하기
worksheet_region = doc.worksheet('corona_region')

#sheet data array list
sheetcontentslist = []

########################################################
#웹크롤링 영역

import requests
from bs4 import BeautifulSoup
import os
import time

def getInfo(_url):
    
    _req = requests.get(_url)
    _req.encoding = 'utf-8'

    _html = _req.text

    if _html == '':
        return
    print(_html)

    
    _soup = BeautifulSoup(_html, 'html.parser')

    tbody_list = _soup.select('tbody')

    #tbody_list[0] : 국내 신고 및 검사 현황(6.25일 0시 기준, 1.3일 이후 누계)
    #tbody_list[1] :  지역별 확진자 현황(6.25일 0시 기준, 1.3일 이후 누계) >
 
   
    ########Regional Data###################################################################
    city_result = ""
    sheet_element = []
    #title_latest = "코로나바이러스감염증-19 국내 발생 현황(2월 27일, 정례브리핑)"
    
            
    city = ["서울","부산","대구","인천","광주","대전","울산","세종","경기","강원","충북","충남","전북","전남","경북","경남","제주","검역"]

    for i in range(len(city)):
        print(i) #0
        #격리자
        isolation = tbody_list[1].select('tr')[1].select('td')[i+2].select('p')[0].select('span')[0].text
        #격리해제
        recover = tbody_list[1].select('tr')[2].select('td')[i+2].select('p')[0].select('span')[0].text
        #사망
        death = tbody_list[1].select('tr')[3].select('td')[i+2].select('p')[0].select('span')[0].text

        print(city[i] + " : " + isolation + ", " + recover + ", " + death  )
        result = [ isolation, death, recover]
        sheetcontentslist.append(result)
      
   
    #UPDATE ALL DATA TO SHEET
    doc.values_update(
        'corona_region!B2', 
        params={'valueInputOption': 'RAW'}, 
        body={'values': sheetcontentslist}
    )
    
    #worksheet_status.append_row([sheetdate, int(total.replace(',','').replace('(','').replace(')','')), int(death.replace(',','').replace('(','').replace(')','')), int(isolation.replace(',','').replace('(','').replace(')','')), int(recover.replace(',','').replace('(','').replace(')','')),int(plus_total.replace(',','').replace('(','').replace(')','')),int(plus_death.replace(',','').replace('(','').replace(')','')),int(plus_isolation.replace(',','').replace('(','').replace(')','')),int(plus_recover.replace(',','').replace('(','').replace(')',''))])
    ########################################################################################



#getInfo("https://www.cdc.go.kr/board/board.es?mid=a20501000000&bid=0015&act=view&list_no=367594&tag=&nPage=1")

getInfo("https://www.cdc.go.kr//board/board.es?mid=a20501000000&bid=0015&act=view&list_no=367606&tag=&nPage=1")

