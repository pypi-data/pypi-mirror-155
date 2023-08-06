#! /usr/bin/python3.8
import json
import logging
from typing import Dict, List

import fasttext
from dostoevsky.models import FastTextSocialNetworkModel
from dostoevsky.tokenization import RegexTokenizer
from nltk import download as nltk_download
from tqdm import tqdm

from sentiment_analyzer.text_cleaner import BaseTextCleaner


class SentimentAnalyzer:
    """Класс сантимент-анализа отзывов
    """

    def __init__(self, text_cleaners: List[BaseTextCleaner] = None) -> None:
        nltk_download('all')
        nltk_download('stopwords')
        logging.info('Downloaded nltk data')
        self.tokenizer = RegexTokenizer()
        logging.info("set tokenizer")
        fasttext.FastText.eprint = lambda x: None

        logging.info("Set sropwords")
        if text_cleaners is not None:
            self.text_cleaners = text_cleaners
            logging.info("Set text cleaners")
        else:
            self.text_cleaners = []
            logging.info("Set text cleaners are empty")

    def __clean_text(self, text: str) -> str:
        """Очистка текста с помощью текст клинеров

        Args:
            text (str): Текст

        Returns:
            str: Очищенный текст
        """
        for cleaner in self.text_cleaners:
            text = cleaner.clean(text)
        return text

    def __prepare_sentiment_list(self, sentiment_list: List[Dict]) -> Dict[str, float]:
        """

        Args:
            sentiment_values (_type_): Список словарей с тональными оценками

        Returns:
            Dict[str,float]: Тональные оценки
        """

        prepared_dict = {}

        for sentiment in sentiment_list:
            neutral = sentiment.get('neutral')
            negative = sentiment.get('negative')
            positive = sentiment.get('positive')
            if neutral is None:
                prepared_dict['neutral'] = 0
            else:
                prepared_dict['neutral'] = sentiment['neutral']
            if negative is None:
                prepared_dict['negative'] = 0
            else:
                prepared_dict['negative'] = sentiment['negative']
            if positive is None:
                prepared_dict['positive'] = 0
            else:
                prepared_dict['positive'] = sentiment['positive']
        return prepared_dict

    def analyze(self, reviews: str) -> str:
        """Сантимент-анализ отзывов

        Args:
            reviws (str): Json с отзывами

        Returns:
            str: Отзывы с тональными оценками json
        """
        reviews_list = json.loads(reviews)
        result_reviews = []
        for review in tqdm(reviews_list):
            model = FastTextSocialNetworkModel(
                tokenizer=self.tokenizer, lemmatize=True)
            text = self.__clean_text(review['text_data'])

            sentiment_list = model.predict([text], k=2)
            sentiment_marks = self.__prepare_sentiment_list(sentiment_list)
            evaluated_review = {**review, **sentiment_marks}
            result_reviews.append(evaluated_review)

        return json.dumps(result_reviews)
