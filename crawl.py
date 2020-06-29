#google sheet dev version
# -*- coding: utf-8 -*-

import gspread
from oauth2client.service_account import ServiceAccountCredentials

##Sheet###############################
scope = [
'https://spreadsheets.google.com/feeds',
'https://www.googleapis.com/auth/drive',
]

json_file_name = 'analog-hull-281314-9e20421b69a5.json'

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
 
   
    ########Regional Data###################################################################
    city_result = ""
    sheet_element = []
    #title_latest = "코로나바이러스감염증-19 국내 발생 현황(2월 27일, 정례브리핑)"
    
            
    city = ["서울","부산","대구","인천","광주","대전","울산","세종","경기","강원","충북","충남","전북","전남","경북","경남","제주","검역"]

    for i in range(len(city)):
        print(i)

        isolation = tbody_list[1].select('tr')[1].select('td')[i+2].select('p')[0].select('span')[0].text
        recover = tbody_list[1].select('tr')[2].select('td')[i+2].select('p')[0].select('span')[0].text
        death = tbody_list[1].select('tr')[3].select('td')[i+2].select('p')[0].select('span')[0].text

        print(city[i] + " : " + isolation + ", " + recover + ", " + death  )
        result = [ isolation, death, recover]
        sheetcontentslist.append(result)
        '''
        #city_result += city[i] + " : " +  tbody_list[2].select('tr')[i+2].select('td')[1].select('p')[0].select('span')[0].text + '\n'

        city_result += city[i] + " : " +  tbody_list[1].select('tr')[4].select('td')[i+2].select('p')[0].select('span')[0].text + '\n'
        #sheet_element.append(tbody_list[2].select('tr')[i+2].select('td')[1].select('p')[0].select('span')[0].text.replace(',',''))
        sheet_element.append(tbody_list[1].select('tr')[4].select('td')[i+2].select('p')[0].select('span')[0].text.replace(',',''))
        #print(city[i] + " : " +  tbody_list[2].select('tr')[i+2].select('td')[1].select('p')[0].select('span')[0].text )
        print(city[i] + " : " +  tbody_list[1].select('tr')[4].select('td')[i+2].select('p')[0].select('span')[0].text )
        '''
   
    #UPDATE ALL DATA TO SHEET
    doc.values_update(
        'corona_region!B2', 
        params={'valueInputOption': 'RAW'}, 
        body={'values': sheetcontentslist}
    )
    
    #worksheet_status.append_row([sheetdate, int(total.replace(',','').replace('(','').replace(')','')), int(death.replace(',','').replace('(','').replace(')','')), int(isolation.replace(',','').replace('(','').replace(')','')), int(recover.replace(',','').replace('(','').replace(')','')),int(plus_total.replace(',','').replace('(','').replace(')','')),int(plus_death.replace(',','').replace('(','').replace(')','')),int(plus_isolation.replace(',','').replace('(','').replace(')','')),int(plus_recover.replace(',','').replace('(','').replace(')',''))])
    ########################################################################################



getInfo("https://www.cdc.go.kr/board/board.es?mid=a20501000000&bid=0015&act=view&list_no=367594&tag=&nPage=1")


'''

while True:
    
    req = requests.get('https://www.cdc.go.kr/board/board.es?mid=a20501000000&bid=0015')
    req.encoding = 'utf-8'
    html = req.text
    
    if html != '':
        soup = BeautifulSoup(html, 'html.parser')
    else: 
        continue

    li_list =  soup.select('#listView > ul > li')
    if len(li_list) > 1:
        url_latest = "https://www.cdc.go.kr" + li_list[1].select('a')[0].attrs['href']
    else: 
        continue

    title_latest = li_list[1].select('a')[0].attrs['title']

    #print(title_latest)

    print("Latest URL : " + url_latest)
    print("Title : " + title_latest)
    
    latest = url_latest
    
#####
    with open(os.path.join(BASE_DIR, 'latest.txt'), 'r+') as f_read:
        before = f_read.readline()
        print("Before in file : " + before)

        if before != latest:
            print("New Post")
            result_text = ""

            credentials = ServiceAccountCredentials.from_json_keyfile_name(json_file_name, scope)
            gc = gspread.authorize(credentials)

            if '현황' in title_latest:
                print("현황 게시글 : " + title_latest)
                result_text = getInfo(url_latest)
                sendTelegramMassge(title_latest +'\n' + url_latest)
                if result_text != None:
                    sendTelegramMassge(result_text)
            else:
                sendTelegramMassge("질본 보도자료 신규 등록" + '\n' + title_latest + '\n' + url_latest)
                       
        else:
            print("No Post")
            #bot.sendMessage(chat_id='439074326', text='No Post')
            
        f_read.close()

    with open(os.path.join(BASE_DIR, 'latest.txt'), 'w+') as f_write:
        f_write.write(latest)
        f_write.close()


    
    time.sleep(60)
'''
