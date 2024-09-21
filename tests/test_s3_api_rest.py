import unittest

import docker
import dotenv
import pytest
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)
dotenv.load_dotenv("../.env.test")


@pytest.fixture(scope='session')
def start_minio_container():
    """Fixture to start a MinIO container before tests and stop it afterward."""
    client = docker.from_env()
    client.images.pull("quay.io/minio/minio")
    # TODO run docker container


# TODO run test docker container with minio instance
class TestDownloadFile(unittest.TestCase):

    def test_download_file_incorrect_bucket_name(self):
        # client.get("")
        pass

    def test_download_file_incorrect_object_name(self):
        # client.get("")
        pass

    def test_download_file_bucket_doesnt_exist(self):
        # client.get("")
        pass

    def test_download_file_object_doesnt_exist(self):
        # client.get("")
        pass


class TestUploadFile(unittest.TestCase):

    def test_upload_file_incorrect_bucket_name(self):
        # client.get("")
        pass

    def test_upload_file_incorrect_object_name(self):
        # client.get("")
        pass

    def test_upload_file_incorrect_large_file(self):
        # client.get("")
        pass

    def test_upload_file_bucket_doesnt_exist(self):
        # client.get("")
        pass

    def test_upload_file_object_doesnt_exist(self):
        # client.get("")
        pass

    def test_upload_file_too_large_file(self):
        # client.get("")
        pass
