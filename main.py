from crawler.WordCrawler import WordCrawler
from crawler.PlayerCrawler import PlayerCrawler
from aws.boto3 import S3Uploader

wordCrawler = WordCrawler()
wordCrawler.getWords()
wordCrawler.getDescriptions()
wordCrawler.saveToCsv()

playerCrawler = PlayerCrawler()
playerCrawler.getPlayers()
playerCrawler.saveToCsv()

s3Uploader = S3Uploader()
s3Uploader.handleUploadCsv("csv/baseball_word.csv", "data/word_raw_data.csv")
s3Uploader.handleUploadCsv("csv/player_info.csv", "data/player_raw_data.csv")