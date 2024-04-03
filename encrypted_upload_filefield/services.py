import logging
import boto3
from cryptography.fernet import Fernet
from botocore.exceptions import ClientError
import os
from dotenv import load_dotenv

load_dotenv()

AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
AWS_SECRET_KEY = os.getenv('AWS_SECRET_KEY')
BUCKET_NAME = os.getenv('BUCKET_NAME')
REGION = os.getenv('AWS_REGION')


class SecurityService:
    def create_new_key(self):
        return Fernet.generate_key()

    def encrypt_file(self, file_content, key):
        file = Fernet(key)
        encrypted_data = file.encrypt(file_content)
        return encrypted_data

    def upload_to_s3(self, filename, encrypted_data):
        s3_client = boto3.client('s3', REGION, aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)

        try:
            response = s3_client.put_object(Bucket=BUCKET_NAME, Key=filename, Body=encrypted_data)
            print(response)
            return True
        except ClientError as e:
            logging.error("Error uploading file to S3: %s", e)
            return False


security_service = SecurityService()