from src.core.common.singleton import Singleton


class MinioError(metaclass=Singleton):
    CONNECTION_ERROR = "errors.minio.connection_error"
    INCORRECT_BUCKET_NAME = "errors.minio.incorrect_bucket_name"
    INCORRECT_OBJECT_NAME = "errors.minio.incorrect_object_name"


class GenericError(Singleton):
    UNKNOWN_ERROR = "errors.generic.unknown_error"
