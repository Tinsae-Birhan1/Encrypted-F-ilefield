import logging
from datetime import datetime
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .serializers import FileUploadSerializer
from .services import SecurityService
import os
import re
from django.http import HttpResponseBadRequest

class FileUpload(APIView):
    serializer_class = FileUploadSerializer
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        uploaded_file = serializer.validated_data['file']
        file_content = uploaded_file.read()

        security_service = SecurityService()
        key = security_service.create_new_key()

        encrypted_file = security_service.encrypt_file(file_content, key)

        save_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'encrypted_files')

        try:
            os.makedirs(save_directory, exist_ok=True)
        except OSError as e:
            logging.error("Error creating directory: %s", e)
            return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        encrypted_file_name = f'{uploaded_file.name}_{timestamp}.encrypted'
        encrypted_file_path = os.path.join(save_directory, encrypted_file_name)

        with open(encrypted_file_path, 'ab') as encrypted_data:
            encrypted_data.write(encrypted_file)

        try:
            if security_service.upload_to_s3(encrypted_file_name, encrypted_file):
                return Response("File encrypted and uploaded to S3", status=status.HTTP_201_CREATED)
            else:
                return Response({'error': 'Failed to upload file to S3'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            logging.error("Error uploading file to S3: %s", e)
            return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
