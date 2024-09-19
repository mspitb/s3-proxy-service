from src.core.translation.translation_manager import TranslationManager


class S3ProxyServiceException(Exception):
    def __init__(self, key: str):
        """
        Basic application exception
        :param key: error key
        """
        self.translation_manager = TranslationManager()
        self.key = key

    def get_message(self):
        return self.translation_manager.translate(self.key)
