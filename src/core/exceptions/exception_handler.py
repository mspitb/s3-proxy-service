from fastapi import Request, Response
from fastapi.responses import JSONResponse
from minio import S3Error
from pydantic import ValidationError
from starlette.status import HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_400_BAD_REQUEST

from src.core.exceptions.error_codes import GenericError
from src.core.exceptions.exception import S3ProxyServiceException
from src.core.translation.translation_manager import TranslationManager
from src.core.common.singleton import Singleton


class ExceptionHandler(metaclass=Singleton):
    translation_manager = TranslationManager()

    @staticmethod
    async def handle(request: Request, exc: Exception) -> Response:
        """
        Generic exception handler
        :param request: request
        :param exc: exception
        :return: response
        """
        if isinstance(exc, S3ProxyServiceException):
            return JSONResponse(status_code=HTTP_400_BAD_REQUEST, content={"message": exc.get_message()})

        if isinstance(exc, S3Error):
            status_code = HTTP_404_NOT_FOUND if exc.code in ['NoSuchBucket',
                                                             'NoSuchKey'] else HTTP_500_INTERNAL_SERVER_ERROR
            return JSONResponse(status_code=status_code, content={"message": exc.args[0]})

        if isinstance(exc, ValidationError) or isinstance(exc, ValueError):
            return JSONResponse(status_code=HTTP_400_BAD_REQUEST, content={"message": exc.args[0]})

        unknown_error_message = ExceptionHandler.translation_manager.translate(GenericError.UNKNOWN_ERROR)
        return JSONResponse(status_code=HTTP_500_INTERNAL_SERVER_ERROR, content={"message": unknown_error_message})
