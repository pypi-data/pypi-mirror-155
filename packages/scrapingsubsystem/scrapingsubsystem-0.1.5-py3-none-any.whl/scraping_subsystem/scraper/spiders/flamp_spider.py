import re
from typing import List

import requests
from scraper.items import Review
from scrapy.spiders.sitemap import Spider


class FlampSpider(Spider):
    """Скраппер для сайта flamp.ru

    Args:
        SitemapSpider (SitemapSpider): Класс Краулера

    Raises:
        ValueError: Нет доступа к flamp.js
    """

    name = 'flamp_spider'

    def parse(self, response):
        review = Review()
        review['review_url'] = response.url
        review['author'] = response.xpath(
            "//a[@class='link name t-text t-text--bold']/text()").get()
        review['review_date'] = response.xpath(
            "//span[@class='ugc-date t-text t-text--small']/text()").get()
        review['text_data'] = response.xpath(
            "//p[@class='t-rich-text__p']").get()
        return review


class GeneratorStartUrlFlampSpider:
    """Генератор стартовых ссылок для краулера flamp.ru
    """

    def __init__(self, name_company_uri: str) -> None:
        """

        Args:
            name_company_uri (str): Идентификатор ресураса компании
        """
        self.name_company_uri = name_company_uri

    def __get_project_codes(self) -> List[str]:
        """Возвращает доменты для сайта flamp.ru
        <name_domain>.flamp.ru

        Raises:
            ValueError: Нет доступа к flamp.js

        Returns:
            List[str]: Список доменов
        """
        flamp_js_url = 'https://flamp.ru/flamp.js?v=0.1'
        response = requests.get(flamp_js_url)
        if response.status_code == 200:
            project_codes_raw = re.search(
                r'PROJECT_CODES\s*=\s*\[.*\'\],', response.text).group(0)
            project_codes_raw = re.search(
                r'\[.*\]', project_codes_raw).group(0)
            project_codes_raw = project_codes_raw.replace('[', '')
            project_codes_raw = project_codes_raw.replace(']', '')
            project_codes_raw = project_codes_raw.replace('\'', '')
            project_codes = project_codes_raw.split(',')
            return project_codes
        else:
            raise ValueError('Can\'t extract project codes from JS')

    def __get_sitemaps_of_sitemaps_urls(self) -> List[str]:
        """Возвращает карты сайтов доменов с картами сайтов

        Returns:
            List[str]: _description_
        """
        project_codes = self.__get_project_codes()
        sitemaps_of_simaps = [
            f'https://{project_code}.flamp.ru/sitemap.xml' for project_code in project_codes]
        return sitemaps_of_simaps

    def __get_url_from_sitemaps(self, sitemaps_of_sitemaps: List[str]) -> List[str]:
        """Парсит карты сайтов с картами сайтов

        Args:
            sitemaps_of_sitemaps (List[str]): Карты сайтов с картами сайтов

        Returns:
            List[str]: Карты сайтов
        """
        urls = []
        for sitemap in sitemaps_of_sitemaps:
            response = requests.get(sitemap)
            if response.status_code == 200:
                tags = re.findall(r"(<loc>)(.*)(</loc>)", response.text)
                urls.extend([tag[1] for tag in tags])
        return urls

    def get_reviews_start_url(self) -> List[str]:
        """Возвращает стартовые страницы для парсинга

        Returns:
            List[str]: Список ссылок
        """
        sitemaps_of_sitemaps = self.__get_sitemaps_of_sitemaps_urls()
        sitemaps = self.__get_url_from_sitemaps(sitemaps_of_sitemaps)
        started_urls = self.__get_url_from_sitemaps(sitemaps)

        pat = re.compile(f"(.*firm)(\/{self.name_company_uri}.*)(\/otzyv.*)")
        filtered = [url for url in started_urls if pat.match(url)]
        return filtered
