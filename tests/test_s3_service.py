import os
import unittest
from unittest.mock import patch, MagicMock

from fastapi import UploadFile
from urllib3.exceptions import HTTPError

from minio import Minio
from starlette.types import Message

from src.models.upload.upload_result import UploadResult
from src.models.upload.upload_request import UploadRequest
from src.core.exceptions.exception import S3ProxyServiceException
from src.service.s3_service import S3Service


class TestS3Service(unittest.TestCase):

    @patch.object(Minio, "__init__", return_value=None)
    def test_download_file_no_exceptions(self, minio_client_init):
        s3_service = S3Service()
        mock_minio_client = MagicMock()
        s3_service.client = mock_minio_client

        mock_download_response = MagicMock()
        mock_download_response.data = b"Hola!"
        mock_minio_client.get_object.return_value = mock_download_response

        file = s3_service.download_file(bucket_name="bucket-name",
                                        object_name="object-name")

        mock_minio_client.get_object.assert_called_once_with(bucket_name="bucket-name",
                                                             object_name="object-name")
        self.assertEqual(b"Hola!", file)

    @patch.object(Minio, "__init__", return_value=None)
    def test_download_file_http_exception(self, minio_client_init):
        s3_service = S3Service()
        mock_minio_client = MagicMock()
        s3_service.client = mock_minio_client

        mock_minio_client.get_object.side_effect = HTTPError("url", 404,
                                                             "exception",
                                                             MagicMock(spec=Message),
                                                             None)
        try:
            s3_service.download_file(bucket_name="bucket-name", object_name="object-name")
            self.fail("HTTPError expected")
        except S3ProxyServiceException as e:
            self.assertEqual('errors.minio.connection_error', e.key)
            mock_minio_client.get_object.assert_called_once_with(bucket_name="bucket-name",
                                                                 object_name="object-name")

    @patch.object(Minio, "__init__", return_value=None)
    def test_upload_file_bucket_must_be_created(self, minio_client_init):
        s3_service = S3Service()
        mock_minio_client = MagicMock()
        mock_file = MagicMock(spec=UploadFile)
        mock_file.file = b"Hola!"
        mock_file.content_type = "content-type"
        mock_upload_request = MagicMock(spec=UploadRequest)
        mock_upload_request.bucket_name = "bucket-name"
        mock_upload_request.object_name = "object-name"
        mock_upload_request.file = mock_file
        mock_upload_result = UploadResult(bucket_name="bucket-name", object_name="object-name")

        s3_service.client = mock_minio_client
        mock_minio_client.bucket_exists.return_value = False
        mock_minio_client.put_object.return_value = mock_upload_result

        with(patch.dict(os.environ, {"CREATE_BUCKET_ON_FILE_UPLOAD": 'True'})):
            result = s3_service.upload_file(mock_upload_request)

        mock_minio_client.bucket_exists.assert_called_once_with(bucket_name="bucket-name")
        mock_minio_client.make_bucket.assert_called_once_with(bucket_name="bucket-name", object_lock=True)
        mock_minio_client.put_object.assert_called_once_with(bucket_name='bucket-name',
                                                             data=b'Hola!',
                                                             object_name='object-name',
                                                             content_type='content-type',
                                                             part_size=10485760,
                                                             length=-1)

        self.assertEqual(mock_upload_result, result)

    @patch.object(Minio, "__init__", return_value=None)
    def test_upload_file_bucket_must_not_be_created(self, minio_client_init):
        s3_service = S3Service()
        mock_minio_client = MagicMock()
        mock_file = MagicMock(spec=UploadFile)
        mock_file.file = b"Hola!"
        mock_file.content_type = "content-type"
        mock_upload_request = MagicMock(spec=UploadRequest)
        mock_upload_request.bucket_name = "bucket-name"
        mock_upload_request.object_name = "object-name"
        mock_upload_request.file = mock_file
        mock_upload_result = UploadResult(bucket_name="bucket-name", object_name="object-name")

        s3_service.client = mock_minio_client
        mock_minio_client.bucket_exists.return_value = True
        mock_minio_client.put_object.return_value = mock_upload_result

        with(patch.dict(os.environ, {"CREATE_BUCKET_ON_FILE_UPLOAD": 'False'})):
            s3_service.upload_file(mock_upload_request)

        mock_minio_client.bucket_exists.assert_called_once_with(bucket_name="bucket-name")
        assert not mock_minio_client.make_bucket.called
        mock_minio_client.put_object.assert_called_once_with(bucket_name='bucket-name',
                                                             data=b'Hola!',
                                                             object_name='object-name',
                                                             content_type='content-type',
                                                             part_size=10485760,
                                                             length=-1)

