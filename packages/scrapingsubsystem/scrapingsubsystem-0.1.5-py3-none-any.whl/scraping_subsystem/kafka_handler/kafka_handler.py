import logging
from datetime import date, datetime
from typing import Dict
from uuid import UUID

from kafka.admin import KafkaAdminClient, NewPartitions, NewTopic
from kafka.errors import InvalidPartitionsError, TopicAlreadyExistsError


class TopicHandler:
    """Класс для работы с топиками
    """
    @staticmethod
    def create_topic(name_topic: str,
                     kafka_address: str) -> None:
        """Создаёт топик в Кафка если он ещё не был создан

        Args:
            name_topic (str): Имя топика
        """
        conf = {'bootstrap_servers': kafka_address}
        client = KafkaAdminClient(**conf)
        topics = []
        topics.append(NewTopic(name_topic, 1, 1))
        try:
            client.create_topics(topics)
            logging.info(f"Successfull creating topic {name_topic}")

        except TopicAlreadyExistsError as topic_already_exists_error:
            logging.error(f"{str(topic_already_exists_error)}")
        else:
            try:
                topic_partitions = {}
                topic_partitions[name_topic] = NewPartitions(total_count=3)
                client.create_partitions(topic_partitions)
                logging.info(f"Successfull creating 3 partitions")
            except InvalidPartitionsError as invalid_partitions_error:
                logging.error(f"{invalid_partitions_error}")


def result_converter(obj: Dict) -> str:
    """Json converter для дат
    Raises:
        TypeError: Object not datetime

    Returns:
        str: _description_
    """
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    if isinstance(obj, UUID):
        return obj.hex
    raise TypeError(f"{type(obj)} not datetime")
