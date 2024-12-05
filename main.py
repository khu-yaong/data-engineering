from crawler.WordCrawler import WordCrawler
from crawler.PlayerCrawler import PlayerCrawler
from crawler.VideoCrawler import VideoCralwer
from aws.boto3 import S3Uploader

wordCrawler = WordCrawler()
wordCrawler.getWords()
wordCrawler.getDescriptions()
wordCrawler.saveToCsv()

playerCrawler = PlayerCrawler()
playerCrawler.getPlayers()
playerCrawler.saveToCsv()

videoCrawler = VideoCralwer()
videoCrawler.getVideos(playlistId="PLz-ZeGBrdzH3riwJYuAXw2H2CpnicIfF4") # KIA (1)
videoCrawler.getVideos(playlistId="PLz-ZeGBrdzH3V0mpqlg5dWM8h4hogL2En") # KIA (2)
videoCrawler.getVideos(playlistId="PLkXXwsF-ojWz3VTp9mYHxhJoCdINkw0UO") # 삼성 (1)
videoCrawler.getVideos(playlistId="PLkXXwsF-ojWyLqf2u0VaVXO-LGCMxyPSe") # 삼성 (2)
videoCrawler.getVideos(playlistId="PLdr_-welsg4eQ2vBlWsINTeXOToaqY3dZ") # LG (1)
videoCrawler.getVideos(playlistId="PLdr_-welsg4d4hKKo3iDHAQlDftuLstSb") # LG (2)
videoCrawler.getVideos(playlistId="PLgbBASjz_-QYm3_dDpIuFEoFHFOL3yUxG") # 두산 (1)
videoCrawler.getVideos(playlistId="PLgbBASjz_-QZueNnOM-V9x-NlAz7i383B") # 두산 (2)
videoCrawler.getVideos(playlistId="PLgbBASjz_-Qatcq4MbIV9u9-1o5YXJxoI") # 두산 (3)
videoCrawler.getVideos(playlistId="PLE8rpoVmjLndvN34XVGER2IYNOp92w--S") # KT (1)
videoCrawler.getVideos(playlistId="PLE8rpoVmjLndsMhCra0ZHbaftWac-YqeD") # KT (2)
videoCrawler.getVideos(playlistId="PLE8rpoVmjLnfFqWzEt3EZ4d3XjgHo8CWZ") # KT (3)
videoCrawler.getVideos(playlistId="PL8_8tSGm7y1BFBaRS8wDu-WgTADcLYmVJ") # SSG (1)
videoCrawler.getVideos(playlistId="PL8_8tSGm7y1Ch1SD1QEIdrF6AhZp9cG5N") # SSG (2)
videoCrawler.getVideos(playlistId="PL8_8tSGm7y1D4cgMXe1FHcQJGRU2sYQcw") # SSG (3)
videoCrawler.getVideos(playlistId="PLe2tqH9V70CO9nSxcNGOInEGkXIXHIJjb") # 롯데 (1)
videoCrawler.getVideos(playlistId="PLe2tqH9V70COQOLCK3ef9W2n4ebCsn6tB") # 롯데 (2)
videoCrawler.getVideos(playlistId="PLH13Vc2FtHHjzoBrp1HYYdQ4BJyEhlVNv") # 한화 (1)
videoCrawler.getVideos(playlistId="PLH13Vc2FtHHg2XTVhdzWaO8Mj6is9_vM-") # 한화 (2)
videoCrawler.getVideos(playlistId="PLH13Vc2FtHHhJZufgqodWKt_hPgMfyaeu") # 한화 (3)
videoCrawler.getVideos(playlistId="PLfsLTyo3tyK_0lGZ7WeTYVnBaRjBREOdd") # NC (1)
videoCrawler.getVideos(playlistId="PLfsLTyo3tyK8cYchJK5Th0uod98ns0wcb") # NC (2)
videoCrawler.getVideos(playlistId="PLfsLTyo3tyK-gWusUOU-Ie3a2Vjnq-i6Q") # NC (3)
videoCrawler.getVideos(playlistId="PLYxgcTlkQOzhSVkpzMGD7dpkH8BRDRJZY") # 키움 (1)
videoCrawler.getVideos(playlistId="PLYxgcTlkQOzi0Pr4hAC0s2ruwezWWhFFF") # 키움 (2)

videoCrawler.saveToCsv()

s3Uploader = S3Uploader()
s3Uploader.handleUploadCsv("csv/baseball_word.csv", "data/word_raw_data.csv")
s3Uploader.handleUploadCsv("csv/player_info.csv", "data/player_raw_data.csv")
s3Uploader.handleUploadCsv("csv/kbo_video.csv", "data/video_raw_data.csv")