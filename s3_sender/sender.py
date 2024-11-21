import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from botocore.client import Config
from dotenv import load_dotenv
import os

class S3Uploader:
    def __init__(self, bucket_name="ptit-iot-picture", region_name="ap-southeast-1"):
        """
        Initializes the S3Uploader with a specific bucket and region.
        
        :param bucket_name: Name of the S3 bucket.
        :param region_name: AWS region for the S3 bucket.
        """
        load_dotenv()

        self.bucket_name = bucket_name
        self.region_name = region_name
        self.s3_client = boto3.client("s3", region_name=self.region_name,aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
        aws_secret_access_key=os.getenv("AWS_SECRET_KEY"))

    def upload_picture(self, file_path, object_name=None):
        """
        Uploads a file to the configured S3 bucket.

        :param file_path: Path to the file to upload.
        :param object_name: S3 object name. If not specified, the file name is used.
        :return: True if the upload was successful, False otherwise.
        """
        if object_name is None:
            object_name = file_path.split("/")[-1]

        try:
            # Upload the file
            self.s3_client.upload_file(file_path, self.bucket_name, object_name)
            print(f"File {file_path} uploaded to {self.bucket_name}/{object_name}")
            return True
        except FileNotFoundError:
            print(f"File {file_path} not found.")
            return False
        except NoCredentialsError:
            print("AWS credentials not available.")
            return False
        except PartialCredentialsError:
            print("Incomplete AWS credentials configuration.")
            return False
        except Exception as e:
            print(f"An error occurred: {e}")
            return False

