import json
import pika

from ...domain.publisher import MessagePublisher


class RabbitMessagePublisher(MessagePublisher):
    def __init__(self, connection_string: str, queue: str):
        self.connection = pika.BlockingConnection(
            pika.URLParameters(connection_string)
        )
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=queue)
        self.__queue = queue

    def publish(self, msg: dict):
        self.channel.basic_publish(
            exchange="", routing_key=self.__queue, body=json.dumps(msg)
        )

    def stop_publishing(self):
        self.connection.close()
