**Encrypted File Upload to S3 with Django**

This Django project provides a secure route for uploading files, encrypting them using Fernet symmetric encryption, and storing them in an Amazon S3 bucket. It ensures data confidentiality by generating a new encryption key for each file upload.

### Setup Instructions

1. **Clone the Repository**

   ```bash
   git clone https://github.com/Tinsae-Birhan1/Encrypted-Filefield.git
   cd Encrypted-Filefield
   ```

2. **Environment Setup**

   - Install Docker and Docker Compose if not already installed.
   - change .env.example to .env and Replace the placeholders in the `.env` file with your AWS credentials and bucket details.

3. **Build and Run Docker Containers**

   ```bash
   docker-compose up
   ```

4. **Access the API**
   The API endpoint for file upload can be accessed at:
   ```
   http://localhost:8000/api/fileupload/
   ```

### How It Works

- **File Upload**: Users can upload files via the provided API endpoint.
- **Encryption**: Upon upload, a new encryption key is generated using Fernet encryption. The file content is then encrypted using this key.
- **Storage**: Encrypted files are stored either in the local file system or in an Amazon S3 bucket, based on the provided configuration.
- **Security**: Private keys are securely managed, and encryption/decryption processes are handled with utmost care to ensure data confidentiality.

### Development Environment

- **Pipenv Installation**: If not using Docker, you can set up the project environment using Pipenv:
  ```bash
  pip install pipenv
  pipenv shell
  pipenv install -r requirements.txt
  ```
- **Run Server**: Start the Django server with:
  ```bash
  python manage.py runserver
  ```

**Access the API**
The API endpoint for file upload can be accessed at:

```
http://localhost:8000/api/fileupload/
```
