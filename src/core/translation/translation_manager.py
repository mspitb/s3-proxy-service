import os
import json
import sys

from src.core.common.singleton import Singleton


class TranslationManager(metaclass=Singleton):
    def __init__(self, default_language="en"):
        self.language = os.getenv("LANGUAGE", default_language)
        self.translations_path = os.path.join(sys.path[0], 'translations', f'{self.language}.json')
        self.translations = self.load_translations()

    def load_translations(self):
        """
        Loads translation file based on application configuration
        :return: translation
        """
        try:
            with open(self.translations_path, "r", encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f"Translation file not found at: {self.translations_path}.")
        except json.JSONDecodeError:
            raise ValueError(f"Failed to decode JSON from the file at: {self.translations_path}.")

    def translate(self, key, **kwargs):
        """
        Get translation string by key
        :param key: translation key
        :param kwargs: additional parameters
        :return: translated string
        """
        keys = key.split(".")
        translation = self.translations
        for k in keys:
            translation = translation.get(k, None)
            if translation is None:
                return key
        return translation.format(**kwargs) if kwargs else translation
