from abc import ABC, abstractmethod

from bs4 import BeautifulSoup as bs
from nltk import sent_tokenize
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


class BaseTextCleaner(ABC):
    """Абстрактный класс клининга текста
    """
    @abstractmethod
    def clean(self, text: str) -> str:
        """Очистка текста перед сантимент-анализом

        Args:
            text (str): Очищаемый текст

        Returns:
            str: Очищенный текст
        """
        raise NotImplementedError


class HtmlTextCleaner(BaseTextCleaner):
    """Очистка текста от html тэгов

    Args:
        BaseTextCleaner (BaseTextCleaner): Абстрактный класс
    """

    def clean(self, text: str) -> str:
        """Очистка текста от тэгов

        Args:
            text (str): Текст

        Returns:
            str: Очищеннный текст
        """
        soup = bs(text)
        return soup.get_text()


class InvisibleSymbolsTextCleaner(BaseTextCleaner):
    """Очистка текста от непечатаемых символов

    Args:
        BaseTextCleaner (BaseTextCleaner): Абстрактный класс
    """

    def clean(self, text: str) -> str:
        """Очистка текста от непечатаемых символов

        Args:
            text (str): Текст

        Returns:
            str: Очищенный текст
        """
        text = text.replace('\t', '')
        text = text.replace('\n\n', '')
        text = text.replace('\n', '')
        return text


class StopWordsTextCleaner(BaseTextCleaner):
    """Очистка текста от стоп слов

    Args:
        BaseTextCleaner (BaseTextCleaner): Абстрактный класс
    """

    def __init__(self, lang: str = 'russian') -> None:
        self.stop_words = stopwords.words('russian')
        self.lang = lang

    def clean(self, text: str) -> str:
        """Очистка текста от стоп слов

        Args:
            text (str): Текст

        Returns:
            str: Очищенный текст
        """

        sentences = sent_tokenize(text, self.lang)
        l_sent = len(sentences)
        for i in range(l_sent):
            tokens = word_tokenize(sentences[i], language=self.lang)
            words = [word for word in tokens if word.isalpha()]
            words = [w for w in words if not w in self.stop_words]
            sentences[i] = " ".join(words)
        return " ".join(sentences)
