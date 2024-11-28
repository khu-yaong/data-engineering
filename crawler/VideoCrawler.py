import sys
from crawler.constant import ENV

sys.path.append(ENV.path)

import os
import csv
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from crawler.constant import VideoConstant


class VideoCralwer : 

    def __init__(self) :
        self.videos = []
        scopes = [VideoConstant.scope]

        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        api_service_name = "youtube"
        api_version = "v3"
        client_secrets_file = VideoConstant.client_secrets

        # Get credentials and create an API client
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            client_secrets_file, scopes)
        flow.run_local_server(port=8080)
        credentials = flow.credentials

        self.youtube = googleapiclient.discovery.build(
            api_service_name, api_version, credentials=credentials)

    def getVideos(self, playlistId) :

        request = self.youtube.playlistItems().list(
            part="snippet",
            playlistId=playlistId,
            maxResults=50
        )

        while request:
            response = request.execute()

            # items가 비어있으면 반복 종료
            if response["items"] == [] :
                break

            # items가 있으면 파싱하여 dictionary 저장
            for items in response["items"] :
                item_dict = {}
                item_dict["title"] = items["snippet"]["title"]
                item_dict["description"] = items["snippet"]["description"]
                item_dict["videoId"] = items["snippet"]["resourceId"]["videoId"]
                self.videos.append(item_dict)
                print(item_dict["videoId"])

            request = self.youtube.search().list_next(request, response)

    def saveToCsv(self) :
        filename = "./csv/kbo_video.csv"

        all_fields = set()
        for player in self.videos:
            all_fields.update(player.keys())
        all_fields = sorted(all_fields)

        with open(filename, mode="a", encoding="utf-8", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=all_fields)
            writer.writeheader()
            for video in self.videos :
                writer.writerow(video)
