import csv
import requests
from bs4 import BeautifulSoup
from crawler.constant import PlayerConstant

class PlayerCrawler :

    def __init__(self) :
        self.playerList = []
        self.url = PlayerConstant.playerDataSource
        self.teams = PlayerConstant.teams
        self.headers = PlayerConstant.headers
        self.host = PlayerConstant.host
        self.recordHeaders = PlayerConstant.recordhHeaders
        self.key_mappings = {
            ## 기본 정보 ##
            "팀명" : "team",
            "등번호" : "no",
            "선수명" : "name",
            "포지션" : "position",
            "생년월일" : "birth",
            "체격" : "hw",
            ## 타자 ##
            "타율" : "avg",
            "홈런" : "hr",
            "안타" : "h",
            "타점" : "rbi",
            "득점" : "r",
            "도루" : "sb",
            "출루율" : "obp",
            "출루율+장타율" : "ops",
            ## 투수 ##
            "평균자책점" : "era",
            "승리" : "w",
            "패배" : "l",
            "세이브" : "sv",
            "홀드" : "hld",
            "이닝" : "ip",
            "삼진" : "so",
            "피안타" : "ha",
            "볼넷" : "bb",
            "이닝당 출루허용률" : "whip"
        }

    def getPlayers(self) :
        for team in self.teams :
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
                
                response = requests.post(self.url, data=data, headers=self.headers, timeout=10)
                if response.status_code == 200 :
                    html = response.text
                    soup = BeautifulSoup(html, "html.parser")

                    table = soup.find("table", {"class": "tEx"})
                    if table :
                    #------------------------------ 1. 선수 정보 파싱 ------------------------------#
                        rows = table.find("tbody").find_all("tr") # tbody의 모든 tr 선택
                        ths = table.find("thead").find_all("th")  # thead의 모든 th 선택
                        for row in rows:
                            player_dict = {}
                            tds = row.find_all("td")
                            for i, th in enumerate(ths):
                                title = th.text.strip()
                                if title in self.key_mappings :
                                    player_dict[self.key_mappings[title]] = tds[i].text.strip()

                    #---------------------------- 2. 선수 기록 정보 파싱 ----------------------------#
                            nameCol = row.find("td").find_next_sibling() # 두 번째 td (선수명)
                            linkTag = nameCol.find("a")
                            playerLink = self.host + linkTag["href"]     # 링크 생성

                            if "Futures" not in playerLink :             # 1군 선수 정보만 포함
                                if linkTag :
                                    self.getPlayerRecords(playerLink=playerLink, player_dict=player_dict)

                    #------------------------------ 3. 선수 정보 추가 ------------------------------#
                                    print(player_dict)
                                    self.playerList.append(player_dict)
                    
                    #----------------------------- 4. 파라미터 업데이트 -----------------------------#
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


    def getPlayerRecords(self, playerLink, player_dict) :
        response = requests.get(playerLink, headers=self.recordHeaders)
        if response.status_code == 200:
            detail_soup = BeautifulSoup(response.text, "html.parser")
            
            detail1 = detail_soup.select_one("#contents > div.sub-content > div.player_records > div:nth-child(3) > table")
            if detail1:
                detail_rows = detail1.find("tbody").find_all("tr")           # tbody의 모든 tr 선택
                ths = detail1.find("thead").find_all("th")                   # thead의 모든 th 선택
                self.extractDataFromTable(detail_rows=detail_rows, player_dict=player_dict, ths=ths)

            detail2 = detail_soup.select_one("#contents > div.sub-content > div.player_records > div:nth-child(4) > table")
            if detail2:
                detail_rows = detail2.find_all("tr")
                ths = detail2.find("thead").find_all("th")
                self.extractDataFromTable(detail_rows=detail_rows, player_dict=player_dict, ths=ths)
                        

    def extractDataFromTable(self, detail_rows, player_dict, ths) :
        for detail_row in detail_rows:
            tds = detail_row.find_all("td")
            for i, th in enumerate(ths):
                a = th.find("a")
                if a :
                    title = a.get("title")
                    if title :
                        if title in self.key_mappings and i < len(tds) :
                            player_dict[self.key_mappings[title]] = tds[i].text.strip()


    def saveToCsv(self) :

        filename = "./csv/player_info.csv"

        all_fields = set()
        for player in self.playerList:
            all_fields.update(player.keys())
        all_fields = sorted(all_fields)

        with open(filename, mode="w", encoding="utf-8", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=all_fields)
            writer.writeheader()
            for player in self.playerList :
                writer.writerow(player)


