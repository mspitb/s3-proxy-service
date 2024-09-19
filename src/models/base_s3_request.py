import re

from pydantic import BaseModel, Field, field_validator, ConfigDict

from src.core.exceptions.exception import S3ProxyServiceException

BUCKET_NAME_PATTERN = r'(?!(^((2(5[0-5]|[0-4][0-9])|[01]?[0-9]{1,2})\.){3}(2(5[0-5]|[0-4][0-9])|[01]?[0-9]{1,2})$|^xn--|.+-s3alias$))^[a-z0-9][a-z0-9.-]{1,61}[a-z0-9]$'


class BaseRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    bucket_name: str = Field()
    object_name: str = Field()

    @field_validator('bucket_name')
    def validate_bucket_name(cls, bucket_name):
        """
        Validates bucket name according to minio rules
        :param bucket_name: minio s3 bucket
        :return: bucket name
        """
        pattern_match = bool(re.fullmatch(BUCKET_NAME_PATTERN, bucket_name))
        contains_consecutive_dots = bool(re.search(r'[!_\-.*\'()/]{2,}', bucket_name))
        if (not pattern_match) or contains_consecutive_dots:
            raise S3ProxyServiceException('errors.minio.incorrect_bucket_name')

        return bucket_name

    @field_validator('object_name')
    def validate_object_name(cls, object_name):
        """
        Validates object name according to minio rules

        :param object_name: minio s3 object
        :return: object name
        """
        if not (1 <= len(object_name) <= 1024) or (not re.fullmatch(r'^[a-zA-Z0-9!\-_.*\'()/]+$', object_name)):
            raise S3ProxyServiceException('errors.minio.incorrect_object_name')

        return object_name
