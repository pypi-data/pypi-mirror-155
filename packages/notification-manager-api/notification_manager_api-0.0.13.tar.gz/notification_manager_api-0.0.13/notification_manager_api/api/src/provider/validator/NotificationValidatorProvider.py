from python_helper import Constant as c
from python_helper import ObjectHelper
from python_framework import Validator, ValidatorMethod, GlobalException, HttpStatus


def buildNotificationValidator():

    @Validator()
    class NotificationValidator:

        @ValidatorMethod(requestClass=[str])
        def validateNotificationApiKey(self, notificationApiKey):
            if ObjectHelper.isNoneOrBlank(notificationApiKey):
                raise GlobalException(
                    message = f'Unauthorized',
                    logMessage = 'Missing current api key',
                    status = HttpStatus.UNAUTHORIZED
                )
            slpitedNotificationApiKey = notificationApiKey.split()
            if not 2 == len(slpitedNotificationApiKey) or not 3 == len(slpitedNotificationApiKey[-1].split(c.DOT)):
                raise GlobalException(
                    message = f'Unauthorized',
                    logMessage = f'Invalid api key: {notificationApiKey}',
                    status = HttpStatus.UNAUTHORIZED
                )

    return NotificationValidator
