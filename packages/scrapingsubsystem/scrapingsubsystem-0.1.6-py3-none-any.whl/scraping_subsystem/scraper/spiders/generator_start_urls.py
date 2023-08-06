from abc import ABC, abstractmethod
from typing import List


class BaseGeneratorStartUrl(ABC):
    """Генератор стартовых ссылок
    """

    @abstractmethod
    def get_reviews_start_url(self) -> List[str]:
        """Генерирует стартовые ссылки

        Returns:
            List[str]: список ссылок
        """
        raise NotImplementedError
