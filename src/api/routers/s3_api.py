import logging
import os
from typing import Optional, Union

from fastapi import APIRouter, Path, Response, Depends
from fastapi import UploadFile, File, Form, HTTPException
from pydantic import ValidationError
from typing_extensions import Annotated

from src.core.common.singleton import Singleton
from src.core.exceptions.exception import S3ProxyServiceException
from src.models.download.download_request import DownloadRequest
from src.models.upload.upload_request import UploadRequest
from src.models.upload.upload_result import UploadResult
from src.service.s3_service import S3Service


class S3APIService(metaclass=Singleton):

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(level=logging.DEBUG)
        self.s3_service: S3Service = S3Service()

    def upload_file_to_bucket(self, upload_request: UploadRequest) -> UploadResult:
        """
        Upload file to minio s3 bucket
        :param upload_request: upload request
        :return: upload result
        """
        return self.s3_service.upload_file(upload_request)

    def download_file_from_bucket(self, bucket_name, object_name) -> bytes:
        """
        Download file from minio s3 bucket
        :param bucket_name: minio bucket name
        :param object_name: minio object name
        :return: file bytes
        """
        return self.s3_service.download_file(bucket_name=bucket_name,
                                             object_name=object_name)


router = APIRouter(prefix='/api',
                   tags=['s3_api'],
                   responses={404: {"description": "Not found"}})

MAX_UPLOAD_SIZE: str = os.getenv("MAX_UPLOAD_FILE_SIZE_MB", "100")
KB_IN_MB: int = 1024


@router.get("/download/{bucket_name}/{object_name}", tags=["download"], responses={
    200: {
        "description": "Downloaded file",
        "content": {
            "application/json": {
                "example": {"The file will be downloaded in json format."}
            },
            "image/jpeg": {
                "example": {"The file will be downloaded in jpeg format."}
            }
        }
    },
    400: {
        "description": "Incorrect bucket name",
        "content": {
            "application/json": {
                "example":
                    {
                        "message": "Incorrect value provided for bucket name. Please, verify minio bucket name rules."
                    }
            }
        }
    },
    404: {
        "description": "Bucket doesn't exist",
        "content": {
            "application/json": {
                "example":
                    {
                        "message": "S3 operation failed; code: NoSuchBucket, message: "
                                   "The specified bucket does not exist, resource: "
                                   "/bucket.lhafsasfasfadfasfasfasdasdasd, request_id: 17F6F971D809D74F, "
                                   "host_id: dd9025bab4ad464b049177c95eb6ebf374d3b3fd1af9251148b658df7ac2e3e8, "
                                   "bucket_name: bucket.lhafsasfasfadfasfasfasdasdasd"
                    }
            }
        }
    }
})
async def download_file_from_bucket(bucket_name: Annotated[Union[Optional[str]], Path(min_length=1)],
                                    object_name: Annotated[Union[Optional[str]], Path(min_length=1)],
                                    s3_api_service: S3APIService = Depends(S3APIService)):
    """
    API method to download file from minio s3 bucket
    """
    s3_api_service.logger.debug(
        f'Received file download request (bucket_name={bucket_name}, object_name={object_name}.'
    )
    try:
        download_request = DownloadRequest(bucket_name=bucket_name, object_name=object_name)
        file_bytes = s3_api_service.download_file_from_bucket(bucket_name=bucket_name, object_name=object_name)
        return Response(content=file_bytes)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/upload", tags=["upload"], responses={
    200: {
        "description": "Upload success",
        "content": {
            "application/json": {
                "example":
                    {
                        "bucket_name": "new-bucket",
                        "object_name": "picture.jpg"
                    }

            }
        }
    },
    400: {
        "description": "Incorrect bucket name",
        "content": {
            "application/json": {
                "example":
                    {
                        "message": "Incorrect value provided for bucket name. Please, verify minio bucket name rules."
                    }
            }
        }
    },
    404: {
        "description": "Bucket doesn't exist",
        "content": {
            "application/json": {
                "example":
                    {
                        "message": "S3 operation failed; code: NoSuchBucket, message: "
                                   "The specified bucket does not exist, resource: "
                                   "/bucket.lhafsasfasfadfasfasfasdasdasd, request_id: 17F6F971D809D74F, "
                                   "host_id: dd9025bab4ad464b049177c95eb6ebf374d3b3fd1af9251148b658df7ac2e3e8, "
                                   "bucket_name: bucket.lhafsasfasfadfasfasfasdasdasd"
                    }
            }
        }
    }
})
async def upload_file(file: UploadFile = File(...),
                      bucket_name: str = Form(...),
                      object_name: str = Form(...),
                      s3_api_service: S3APIService = Depends(S3APIService)):
    """
    Uploads file to minio s3 bucket
    """
    s3_api_service.logger.debug(
        f"Received upload file request (bucket_name={bucket_name}, object_name={object_name})."
    )
    try:
        upload_request = UploadRequest(bucket_name=bucket_name,
                                       object_name=object_name,
                                       file=file)

        if file.size.real / KB_IN_MB > int(MAX_UPLOAD_SIZE):
            raise S3ProxyServiceException(f"Upload file size can't be more then {MAX_UPLOAD_SIZE} MB(s).")

        return s3_api_service.upload_file_to_bucket(upload_request).to_response()

    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
