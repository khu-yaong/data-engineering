import csv
import requests
from bs4 import BeautifulSoup
from crawler.constant import PlayerConstant

# URL 설정
url = PlayerConstant.playerDataSource

# KBO Teams
teams = PlayerConstant.teams

# Header 설정
headers = PlayerConstant.headers

playerList = []

for team in teams :

    data = {
        "ctl00$ctl00$ctl00$cphContents$cphContents$cphContents$hfPage": "1",
        "ctl00$ctl00$ctl00$cphContents$cphContents$cphContents$ddlPosition": "",
        "ctl00$ctl00$ctl00$cphContents$cphContents$cphContents$txtSearchPlayerName": "",
        "__VIEWSTATE": PlayerConstant.viewState,
        "__VIEWSTATEGENERATOR": PlayerConstant.viewStateGenerator,
        "__EVENTVALIDATION": PlayerConstant.eventValidation,
        "__ASYNCPOST": "true"
    }

    for page in range(1, 11) :
        data["ctl00$ctl00$ctl00$cphContents$cphContents$cphContents$ScriptManager1"] = f"ctl00$ctl00$ctl00$cphContents$cphContents$cphContents$udpRecord|ctl00$ctl00$ctl00$cphContents$cphContents$cphContents$ucPager$btnNo{page}"
        data["__EVENTTARGET"] = f"ctl00$ctl00$ctl00$cphContents$cphContents$cphContents$ucPager$btnNo{page}"
        data["ctl00$ctl00$ctl00$cphContents$cphContents$cphContents$ddlTeam"] = f"{team}"
        
        response = requests.post(url, data=data, headers=headers, timeout=10)
        if response.status_code == 200 :
            html = response.text
            soup = BeautifulSoup(html, "html.parser")

            table = soup.find("table", {"class": "tEx"})
            if table :
            #------------------------------ 1. 선수 정보 파싱 ------------------------------#
                rows = table.find("tbody").find_all("tr") # tbody의 모든 tr(행) 선택
                for row in rows:
                    cols = row.find_all("td")  # td(열) 선택
                    cols = [col.text.strip() for col in cols]  # 텍스트만 추출하고 공백 제거

            #---------------------------- 2. 선수 기록 정보 파싱 ----------------------------#
                    nameCol = row.find("td").find_next_sibling() # 두 번째 td (선수명)
                    linkTag = nameCol.find("a")
                    if linkTag :
                        playerLink = PlayerConstant.host + linkTag["href"] # 링크 생성

                        response = requests.get(playerLink, headers=PlayerConstant.recordhHeaders)
                        if response.status_code == 200:
                            detail_soup = BeautifulSoup(response.text, "html.parser")
                            
                            detail1 = detail_soup.select_one("#contents > div.sub-content > div.player_records > div:nth-child(3) > table")
                            if detail1:
                                detail_rows = detail1.find_all("tr")
                                for detail_row in detail_rows:
                                    detail_cols = detail_row.find_all("td")
                                    for col in detail_cols :
                                        cols.append(col.text.strip())
                            
                            detail2 = detail_soup.select_one("#contents > div.sub-content > div.player_records > div:nth-child(4) > table")
                            if detail2:
                                detail_rows = detail2.find_all("tr")
                                for detail_row in detail_rows:
                                    detail_cols = detail_row.find_all("td")
                                    for col in detail_cols :
                                        cols.append(col.text.strip())

            #------------------------------ 3. 선수 정보 추가 ------------------------------#
                    playerList.append(cols)
            
            # HTML 최하단의 텍스트 추출
            raw_text = soup.text

            # __VIEWSTATE 추출
            viewstate_start = raw_text.find("|hiddenField|__VIEWSTATE|") + len("|hiddenField|__VIEWSTATE|")
            viewstate_end = raw_text.find("|", viewstate_start)
            viewstate = raw_text[viewstate_start:viewstate_end]

            # __EVENTVALIDATION 추출
            eventvalidation_start = raw_text.find("|hiddenField|__EVENTVALIDATION|") + len("|hiddenField|__EVENTVALIDATION|")
            eventvalidation_end = raw_text.find("|", eventvalidation_start)
            eventvalidation = raw_text[eventvalidation_start:eventvalidation_end]

            # ViewState Update
            data["__VIEWSTATE"] = viewstate
            data["__EVENTVALIDATION"] = eventvalidation

# csv 파일 저장
filename = "./csv/player_info.csv"
with open(filename, mode="w", encoding="utf-8", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["등번호", "선수명", "팀명", "포지션", "생년월일", "체격", "출신교", \
                    '팀명', 'AVG/ERA', 'G/G', 'PA/CG', 'AB/SHO', 'R/W', 'H/L', '2B/SV', \
                    '3B/HLD', 'HR/WPCT', 'TB/TBF', 'RBI/NP', 'SB/IP', 'CS/H', 'SAC/2B', \
                    'SF/3B', 'BB/HR', 'IBB/SAC', 'HBP/SF', 'SO/BB', 'GDP/IBB', 'SLG/SO', \
                    'OBP/WP', 'E/BK', 'SB%/R', 'MH/ER', 'OPS/BSV', 'RISP/WHIP', 'PH-BA/AVG', '/QS'])
    writer.writerows(playerList)
    