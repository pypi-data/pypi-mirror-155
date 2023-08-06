from python_framework import HttpStatus
from queue_manager_api import MessageListener, MessageListenerMethod

from ApiKeyContext import ApiKeyContext
from config import QueueConfig
import NotificationDto


@MessageListener(
    timeout = QueueConfig.API_NOTIFICATIONS_LISTENER_TIMEOUT
    , muteLogs = False
    # , logRequest = True
    # , logResponse = True
)
class NotificationManagerListener:

    @MessageListenerMethod(url = '/listener/notifications',
        requestClass = [[NotificationDto.NotificationRequestDto]],
        apiKeyRequired=[ApiKeyContext.ADMIN, ApiKeyContext.USER, ApiKeyContext.API]
        , runInAThread = True
        # , logRequest = True
        # , logResponse = True
    )
    def acceptAll(self, dtoList):
        return self.service.notificationManager.acceptAll(dtoList), HttpStatus.ACCEPTED
