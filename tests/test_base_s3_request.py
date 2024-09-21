import unittest

from src.core.exceptions.exception import S3ProxyServiceException
from src.models.base_s3_request import BaseRequest


class TestBaseRequest(unittest.TestCase):
    BUCKET_NAME_ERROR_MESSAGE: str = (
        "Incorrect value provided for bucket name. Please, verify minio bucket name rules."
    )
    OBJECT_NAME_ERROR_MESSAGE: str = (
        "Incorrect value provided for object name. Please, verify minio bucket name rules."
    )

    def test_bucket_name_is_empty(self):
        with self.assertRaises(S3ProxyServiceException) as context:
            BaseRequest(bucket_name="", object_name="object")
        self.assertEqual(
            self.BUCKET_NAME_ERROR_MESSAGE, str(context.exception.get_message())
        )

    def test_bucket_name_too_short(self):
        with self.assertRaises(S3ProxyServiceException) as context:
            BaseRequest(bucket_name="ab", object_name="object")
        self.assertEqual(
            self.BUCKET_NAME_ERROR_MESSAGE, str(context.exception.get_message())
        )

    def test_bucket_name_too_long(self):
        with self.assertRaises(S3ProxyServiceException) as context:
            BaseRequest(bucket_name="a" * 64, object_name="object")
        self.assertEqual(
            self.BUCKET_NAME_ERROR_MESSAGE, str(context.exception.get_message())
        )

    def test_bucket_name_invalid_pattern(self):
        with self.assertRaises(S3ProxyServiceException) as context:
            BaseRequest(bucket_name="Invalid_Bucket!", object_name="object")
        self.assertEqual(
            self.BUCKET_NAME_ERROR_MESSAGE, str(context.exception.get_message())
        )

    def test_bucket_name_valid(self):
        try:
            BaseRequest(bucket_name="valid-bucket.name", object_name="object")
        except S3ProxyServiceException:
            self.fail(
                "S3ProxyServiceException raised unexpectedly for a valid bucket name!"
            )

    def test_bucket_name_starts_with_xn(self):
        with self.assertRaises(S3ProxyServiceException) as context:
            BaseRequest(bucket_name="xn--bucket", object_name="object")
        self.assertEqual(
            self.BUCKET_NAME_ERROR_MESSAGE, str(context.exception.get_message())
        )

    def test_bucket_name_ends_with_s3alias(self):
        with self.assertRaises(S3ProxyServiceException) as context:
            BaseRequest(bucket_name="bucket-s3alias", object_name="object")
        self.assertEqual(
            self.BUCKET_NAME_ERROR_MESSAGE, str(context.exception.get_message())
        )

    def test_bucket_name_contains_adjacent_periods(self):
        with self.assertRaises(S3ProxyServiceException) as context:
            BaseRequest(bucket_name="bucket..name", object_name="object")
        self.assertEqual(
            self.BUCKET_NAME_ERROR_MESSAGE, str(context.exception.get_message())
        )

    def test_bucket_name_period_adjacent_to_hyphen(self):
        with self.assertRaises(S3ProxyServiceException) as context:
            BaseRequest(bucket_name="bucket.-name", object_name="object")
        self.assertEqual(
            self.BUCKET_NAME_ERROR_MESSAGE, str(context.exception.get_message())
        )

    def test_bucket_name_formatted_as_ip(self):
        with self.assertRaises(S3ProxyServiceException) as context:
            BaseRequest(bucket_name="192.168.1.1", object_name="object")
        self.assertEqual(
            self.BUCKET_NAME_ERROR_MESSAGE, str(context.exception.get_message())
        )

    def test_object_name_is_empty(self):
        with self.assertRaises(S3ProxyServiceException) as context:
            BaseRequest(bucket_name="valid-bucket.name", object_name="")
        self.assertEqual(
            self.OBJECT_NAME_ERROR_MESSAGE, str(context.exception.get_message())
        )

    def test_object_name_valid(self):
        try:
            BaseRequest(bucket_name="valid-bucket", object_name="object_name")
        except S3ProxyServiceException:
            self.fail("Unexpected validation exception raised.")
