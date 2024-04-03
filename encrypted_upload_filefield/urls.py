from django.urls import path
from .views import FileUpload

urlpatterns = [
    path('fileupload/', FileUpload.as_view(), name='file_upload'),
]