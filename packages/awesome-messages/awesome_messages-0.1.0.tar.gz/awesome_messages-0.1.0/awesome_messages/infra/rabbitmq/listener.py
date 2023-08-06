import json
import pika

from ...domain.handler import MessageHandler
from ...domain.listener import MessageListener


class RabbitMessageListener(MessageListener):
    def __init__(
        self,
        connection_string: str,
        queue: str,
        message_handler: MessageHandler,
    ):
        self.__message_handler = message_handler
        self.connection = pika.BlockingConnection(
            pika.URLParameters(connection_string)
        )
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=queue)
        self.channel.basic_consume(queue, self.on_reception, auto_ack=True)

    def on_reception(self, ch, method, properties, body):
        self.__message_handler.on_msg(json.loads(body.decode()))

    def start_listening(self):
        self.channel.start_consuming()

    def stop_listening(self):
        self.channel.stop_consuming()
        self.connection.close()
