from python_framework import Controller, ControllerMethod, HttpStatus
from queue_manager_api import MessageDto

import NotificationDto
from ApiKeyContext import ApiKeyContext


@Controller(url = '/async/notification', tag='Async Notification', description='Async notification controller'
    # , logRequest = True
    # , logResponse = True
)
class NotificationController:

    @ControllerMethod(url = '/',
        requestClass = [[NotificationDto.NotificationRequestDto]],
        responseClass = [MessageDto.MessageCreationRequestDto],
        apiKeyRequired=[ApiKeyContext.ADMIN, ApiKeyContext.USER, ApiKeyContext.API]
        # , logRequest = True
        # , logResponse = True
    )
    def post(self, dtoList):
        return self.service.notification.notifyAllByCurrentApiKey(dtoList), HttpStatus.ACCEPTED
