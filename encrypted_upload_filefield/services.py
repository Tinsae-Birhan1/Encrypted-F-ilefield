import logging
import boto3
from cryptography.fernet import Fernet
from botocore.exceptions import ClientError
import os
from dotenv import load_dotenv
from django.conf import settings
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

load_dotenv()

AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
AWS_SECRET_KEY = os.getenv('AWS_SECRET_KEY')
BUCKET_NAME = os.getenv('BUCKET_NAME')
REGION = os.getenv('AWS_REGION')


class SecurityService:
    def __init__(self):
        self.key_management_service = KeyManagementService()
    
    def create_new_key(self):
        return Fernet.generate_key()

    def retrieve_private_key(self):
        return self.key_management_service.retrieve_private_key()

    def encrypt_file(self, file_content, key):
        file = Fernet(key)
        encrypted_data = file.encrypt(file_content)
        return encrypted_data

    def decrypt_file(self, encrypted_data, key):
        try:
            if not isinstance(key, bytes) or len(key) != 32:
                raise ValueError("Invalid Fernet key provided")

            fernet = Fernet(key)
            decrypted_data = fernet.decrypt(encrypted_data)
            return decrypted_data
        except Exception as e:
            logging.error("Error decrypting file: %s (encrypted_data: %s)", e, encrypted_data[:16])  # Truncate encrypted_data for security
            raise DecryptionError("Failed to decrypt file") 

    def upload_to_s3(self, filename, encrypted_data):
        s3_client = boto3.client('s3', REGION, aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)

        try:
            response = s3_client.put_object(Bucket=BUCKET_NAME, Key=filename, Body=encrypted_data)
            print(response)
            return True
        except ClientError as e:
            logging.error("Error uploading file to S3: %s", e)
            return False


class KeyManagementService:
    @staticmethod
    def generate_rsa_key_pair():
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        public_key = private_key.public_key()
        return private_key, public_key

    @staticmethod
    def store_private_key(private_key):
        serialized_private_key = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        with open(settings.KEY_STORAGE_PATH, 'wb') as key_file:
            key_file.write(serialized_private_key)

    @staticmethod
    def retrieve_private_key():
        with open(settings.KEY_STORAGE_PATH, 'rb') as key_file:
            private_key_data = key_file.read()
            private_key = serialization.load_pem_private_key(
                private_key_data,
                password=None,
                backend=default_backend()
            )
        return private_key
