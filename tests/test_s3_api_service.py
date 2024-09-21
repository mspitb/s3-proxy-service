import unittest
from unittest.mock import patch, MagicMock

from src.models.download.download_request import DownloadRequest
from src.api.routers.s3_api import S3APIService
from src.models.upload.upload_request import UploadRequest
from src.models.upload.upload_result import UploadResult


class TestS3APIService(unittest.TestCase):

    @patch('src.api.routers.s3_api.S3Service')
    def test_upload_file_to_bucket(self, mock_s3_service):
        mock_upload_result = MagicMock(spec=UploadResult)
        mock_upload_request = MagicMock(spec=UploadRequest)
        mock_s3_service = mock_s3_service.return_value
        mock_s3_service.upload_file.return_value = mock_upload_result

        result = S3APIService().upload_file_to_bucket(mock_upload_request)

        mock_s3_service.upload_file.assert_called_once_with(mock_upload_request)
        self.assertEqual(result, mock_upload_result)

    @patch('src.api.routers.s3_api.S3Service')
    def test_download_file_to_bucket(self, mock_s3_service):
        download_request = DownloadRequest(bucket_name="bucket-name", object_name="object-name")
        mock_s3_service = mock_s3_service.return_value
        download_response = MagicMock(spec=bytes)
        mock_s3_service.download_file.return_value = download_response

        result = S3APIService().download_file_from_bucket(download_request)

        mock_s3_service.download_file.assert_called_once_with(bucket_name="bucket-name",
                                                              object_name="object-name")
        self.assertEqual(result, download_response)
