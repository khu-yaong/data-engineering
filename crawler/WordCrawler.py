import csv
import requests
import re
#from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
from dto.WordDTO import Word
from crawler.constant import HttpConstant

class WordCralwer :
    
    def __init__(self) :
        self.headers = HttpConstant.headers
        self.dataSource = HttpConstant.dataSource

    def getWords(self) :
        wordData = requests.get(self.dataSource, headers=self.headers)
        wordHtml = wordData.text
        wordSoup = BeautifulSoup(wordHtml, "html.parser")

        for i in range(1, 4):
            for j in range(1, 20):
                # 야구 용어 url이 담긴 <a> 추출
                a_href = wordSoup.select_one(f"#tab0{i}_cont > div > ul > li:nth-child({j}) > a")
                if a_href:
                    word = a_href.text.strip()
                    url = a_href.get("href")
                    Word.words.append(Word(word, url))

    def getDescriptions(self) :
        for word in Word.words :
            descriptionData = requests.get(word.url, headers=self.headers)
            descriptionHtml = descriptionData.text
            descriptionSoup = BeautifulSoup(descriptionHtml, "html.parser")
            
            summary = descriptionSoup.select_one("#size_ct > dl")
            if summary :
                description = re.sub(r"^요약\s*", "", summary.text.strip().replace("\n", " "))
                word.description += f"{description}\n"
                
                
            txt = descriptionSoup.select_one("#size_ct > p")
            if txt : 
                word.setDescription(txt)

            t_txt1 = descriptionSoup.select_one("#naml_contents_container > p:nth-child(1)")
            if t_txt1 : 
                word.setDescription(t_txt1)
            else :
                t_txt2 = descriptionSoup.select_one("#naml_contents_container > p:nth-child(2)")
                if t_txt2 : 
                    word.setDescription(t_txt2)

            # exception
            area = descriptionSoup.select_one("#SEDOC-1491514668704--1083807156 > div.se_component_wrap.sect_dsc.__se_component_area > div > div > div > div > div > div > p")
            if area : 
                word.setDescription(area)

            # exception
            double_play = descriptionSoup.select_one("#size_ct > div:nth-child(1) > dl > dd:nth-child(2)")
            if double_play : 
                word.setDescription(double_play)

    def saveToCsv(self) :
        filename = "./csv/baseball_word.csv"
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=["word", "url", "description"])
            writer.writeheader()
            for word in Word.words :
                writer.writerow(word.toDict())
    