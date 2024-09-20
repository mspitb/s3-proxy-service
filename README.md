# S3 Proxy Service

<div style="text-align:justify;max-width: 800px"> This is a FastAPI-based proxy service for interacting with an S3-compatible storage (MinIO). 
The service allows users to upload and download files to/from the MinIO instance, with validations and exception handling.

## Features

- File upload to MinIO bucket
- File download from MinIO bucket
- Validation for bucket and object names
- Exception handling for different error scenarios

## Prerequisites

- Python 3.9+
- MinIO
- Docker (optional)

## Setup Instructions

1. Clone the Repository:
    ```bash
       git clone https://github.com/mspitb/s3-proxy-service.git
       cd s3-proxy-service
    ```

2. Set Up Virtual Environment: </br>
    ```bash
      python -m venv venv
      source venv/bin/activate # For Linux/MacOS
      venv\Scripts\activate # For Windows
   ```

3. Install Dependencies: </br>
    ```bash
      pip install -r requirements.txt
   ```

## Configure MinIO

Run MinIO locally using Docker following instruction:
[ReadMe.md](infrastructure/docker/minio/ReadMe.md)


# Additional Settings

## .env

### Explanation of .env Variables:
- MINIO_HOST: The host and port where your MinIO instance is running.
- MINIO_ACCESS_KEY: The access key for MinIO authentication.
- MINIO_SECRET_KEY: The secret key for MinIO authentication.
- MAX_UPLOAD_FILE_SIZE_MB: The maximum file size allowed for uploads.
- CREATE_BUCKET_ON_FILE_UPLOAD: If set to True, the service will create a bucket automatically if it does not exist when
uploading a file.

## Running the Application

### Run server:
```bash
uvicorn main:app --reload

```

This will start the FastAPI application. You can access the API documentation via:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Running Tests

```bash
pytest
```

</div>

