import logging
import os

from dotenv import load_dotenv
from minio import Minio
from src.core.common.singleton import Singleton
from src.models.upload.upload_result import UploadResult
from src.models.upload.upload_request import UploadRequest
from src.core.exceptions.exception import S3ProxyServiceException
from urllib3.exceptions import HTTPError


class S3Service(metaclass=Singleton):
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.client = Minio(endpoint=os.getenv("MINIO_HOST"),
                            access_key=os.getenv("MINIO_ACCESS_KEY"),
                            secret_key=os.getenv("MINIO_SECRET_KEY"),
                            secure=False)

    def download_file(self, bucket_name: str, object_name: str):
        """
        Downloads file from minio s3 bucket
        :param bucket_name: minio s3 bucket name
        :param object_name: minio s3 object name
        :return: file bytes
        """
        try:
            self.logger.debug(f"Start downloading file {object_name} from {bucket_name}.")
            result = self.client.get_object(bucket_name=bucket_name, object_name=object_name)
            return result.data
        except HTTPError:
            raise S3ProxyServiceException("errors.minio.connection_error")

    def upload_file(self, upload_request: UploadRequest) -> UploadResult:
        """
        Uploads file to minio s3
        :param upload_request: request with information about bucket/object
        """
        self.logger.debug(f"Start uploading file {upload_request.object_name} to {upload_request.bucket_name}.")
        bucket_name = upload_request.bucket_name
        if not self.__bucket_exist(bucket_name):
            if os.getenv('CREATE_BUCKET_ON_FILE_UPLOAD', 'False').lower() == 'true':
                self.__create_bucket(bucket_name=bucket_name)
        try:
            self.client.put_object(bucket_name=bucket_name,
                                   data=upload_request.file.file,
                                   object_name=upload_request.object_name,
                                   content_type=upload_request.file.content_type,
                                   part_size=10 * 1024 * 1024,
                                   length=-1)
        except HTTPError:
            raise S3ProxyServiceException("errors.minio.connection_error")

        return UploadResult(bucket_name=bucket_name, object_name=upload_request.object_name)

    def __create_bucket(self, bucket_name: str, object_lock: bool = True):
        """
        Creates bucket on minio s3 instance
        :param bucket_name: name of the bucket to be created
        :param object_lock: locking object (see minio spec)
        """
        try:
            self.client.make_bucket(bucket_name=bucket_name, object_lock=object_lock)
        except HTTPError:
            raise S3ProxyServiceException("errors.minio.connection_error")

    def __bucket_exist(self, bucket_name: str):
        """
        Verifies existence of the bucket by bucket name
        :param bucket_name: name of the bucket to be verified
        :return: existence result True/False
        """
        try:
            bucket_exists = self.client.bucket_exists(bucket_name=bucket_name)
            return True if bucket_exists else False
        except Exception as e:
            self.logger.error(f'Error in S3Service: {e}')
            raise e
