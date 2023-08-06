import json
import logging
import tempfile
from typing import Dict

from kafka import KafkaProducer
from scrapy import Spider
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from kafka_handler.kafka_handler import TopicHandler, result_converter
from scraper.spiders.flamp_spider import (FlampSpider,
                                          GeneratorStartUrlFlampSpider)
from sentiment_analyzer.analyzer import SentimentAnalyzer
from sentiment_analyzer.text_cleaner import (BaseTextCleaner, HtmlTextCleaner,
                                             InvisibleSymbolsTextCleaner,
                                             StopWordsTextCleaner)


def extract_reviews(spider: Spider, spider_settings: Dict = None,
                    crawl_settings: Dict = None) -> str:
    """С помощью конкретного паука извлекает отзывы компании

    Args:
        spider (Spider): Паук
        spider_settings (Dict): Настройки для класса паука
        crawl_settings (Dict): Настройки для CrawlerProcess

    Returns:
        str: json с отзывами
    """
    with tempfile.TemporaryDirectory() as tempdir:
        result_file_path = f"{tempdir}/reviews.json"
        if spider_settings is None:
            settings = {
                'FEED_FORMAT': "json",
                "FEED_URI": result_file_path}
        else:
            settings = spider_settings
        if crawl_settings is not None:
            crawling_settings = crawl_settings

        crawler_settings = Settings(settings)
        crawler_settings.setmodule(crawler_settings)

        process = CrawlerProcess(settings=crawler_settings)
        process.crawl(spider, **crawling_settings)
        process.start(stop_after_crawl=True)

        with open(result_file_path, 'r', encoding='utf-8') as f:
            result = f.read()
    return result


def calculation_sentiment_marks(reviews: str) -> str:
    """Вычисление тональных оценок

    Args:
        reviews (str): Json с отзывами

    Returns:
        str: _description_
    """
    cleaners = [HtmlTextCleaner(), InvisibleSymbolsTextCleaner(),
                StopWordsTextCleaner()]

    sentiment_analyzer = SentimentAnalyzer(cleaners)
    return sentiment_analyzer.analyze(reviews)


def load_to_kafka(data_reviews: str, key: str,
                  kafka_address: str,
                  name_topic: str = "reviews") -> None:
    """Загружает результаты в Кафку

    Args:
        data_reviews (str): Отзывы с оценками
        key (str): Ключ пакета
        kafka_address (str): адресс Кафки
        name_topic (str, optional): _description_. Defaults to "reviews".
    """
    records = json.loads(data_reviews)

    TopicHandler.create_topic(name_topic, kafka_address)
    producer = KafkaProducer(
        bootstrap_servers=[kafka_address], compression_type='gzip',
        value_serializer=lambda v: json.dumps(
            v, default=result_converter).encode('utf-8')
    )

    for record in records:
        producer.send(topic=name_topic,
                      key=bytes(f"{key}", 'utf-8'), value=record).get(timeout=10)
    producer.flush()
    logging.info(
        f"Loaded {len(records)} unmatched results {key} to Apache Kafka")


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.NOTSET,
        filename="crawler_logs.log",
        format="%(asctime)s - %(module)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s",
        datefmt='%H:%M:%S',
    )

    generator_start_urls = GeneratorStartUrlFlampSpider(
        'kfc_set_restoranov_bystrogo_obsluzhivaniya')
    start_urls = generator_start_urls.get_reviews_start_url()
    reviews = extract_reviews(FlampSpider, crawl_settings={
                              'start_urls': start_urls[:100]})
    reviews = calculation_sentiment_marks(reviews)
    load_to_kafka(reviews, 'flamp.ru/kfc', 'localhost:9092')
