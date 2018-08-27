import sys
import pika #amqp library for RabbitMq connections
import json
import LoggingConfig

from AppSettingsProvider import AppSettingsProvider
from MessageProcessingService import MessageProcessingService
from QueueConsumer import QueueConsumer

def main(argv):

    appSettings = AppSettingsProvider()

    messageProcessingService = MessageProcessingService(
        requestServer = appSettings.get_request_server())

    rabbitMqService = QueueConsumer(
        rabbitMqCredentials=appSettings.get_rabbitMq_credentials(),
        rabbitMqQueue=appSettings.get_rabbitMq_queue(),
        messageProcessingFunction = messageProcessingService.process_message)

    try:
        print('Welcome to Pi HomeHud service')
        #rabbitMqService.run()
    except KeyboardInterrupt:
        #rabbitMqService.stop()
        print('Closing Pi HomeHud service')


if __name__ == '__main__':
    main(sys.argv[1:])