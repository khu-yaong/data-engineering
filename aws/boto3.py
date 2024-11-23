import boto3
import boto3.session
import aws.config as config

class S3Uploader :

    def __init__(self) :
        self.AWS_ACCESS_KEY = config.AWS_ACCESS_KEY
        self.AWS_SECRET_ACCESS_KEY = config.AWS_SECRET_ACCESS_KEY
        self.BUCKET_NAME = config.BUCKET_NAME

        try:
            client = boto3.client(
                service_name = "s3",
                region_name = "ap-northeast-2",
                aws_access_key_id = self.AWS_ACCESS_KEY,
                aws_secret_access_key = self.AWS_SECRET_ACCESS_KEY
            )
            self.s3_client = client
        except Exception as e:
            print(e)

    def handleUploadCsv(self, origin, filename) :
        try:
            self.s3_client.upload_file(origin, config.BUCKET_NAME, filename)
        except Exception as e:
            print(e)
