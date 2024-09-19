from fastapi import UploadFile
from pydantic import Field

from models.base_s3_request import BaseRequest


class UploadRequest(BaseRequest):
    file: UploadFile = Field(exclude=True)
