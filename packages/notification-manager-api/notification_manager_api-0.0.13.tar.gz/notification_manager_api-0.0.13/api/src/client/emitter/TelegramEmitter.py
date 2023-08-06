from queue_manager_api import MessageEmitter, MessageEmitterMethod
from python_framework import JwtConstant

from config import QueueConfig


@MessageEmitter(
    url = QueueConfig.SEND_TELEGRAM_EMITTER_BASE_URL,
    headers = {
        JwtConstant.DEFAULT_JWT_API_KEY_HEADER_NAME: f'Bearer {QueueConfig.SEND_TELEGRAM_EMITTER_API_KEY}'
    },
    timeout = QueueConfig.SEND_TELEGRAM_EMITTER_TIMEOUT
    # , muteLogs = False
    # , logRequest = True
    # , logResponse = True
)
class TelegramEmitter:

    @MessageEmitterMethod(
        queueKey = QueueConfig.SEND_TELEGRAM_QUEUE_KEY,
        requestClass=[[dict]]
        # , logRequest = True
        # , logResponse = True
    )
    def messageAll(self, dtoList):
        self.emit(
            messageHeaders = {
                JwtConstant.DEFAULT_JWT_API_KEY_HEADER_NAME: f'Bearer {QueueConfig.TELEGRAM_MANAGER_API_API_KEY}'
            },
            body = dtoList
        )
