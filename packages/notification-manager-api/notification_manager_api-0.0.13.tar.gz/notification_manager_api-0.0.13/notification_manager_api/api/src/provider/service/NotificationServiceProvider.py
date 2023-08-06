from python_helper import Constant as c
from python_helper import ObjectHelper, log
from python_framework import Service, ServiceMethod, FlaskUtil, JwtConstant, EnumItem

try:
    from config import NotificationConfig
    from enumeration.NotificationSeverity import NotificationSeverity
    from enumeration.NotificationDestiny import NotificationDestiny
    from constant import NotificationConstant
    import NotificationDto
except:
    try:
        from notification_manager_api.api.src.config import NotificationConfig
        from notification_manager_api.api.src.enumeration.NotificationSeverity import NotificationSeverity
        from notification_manager_api.api.src.enumeration.NotificationDestiny import NotificationDestiny
        from notification_manager_api.api.src.constant import NotificationConstant
        from notification_manager_api.api.src.dto import NotificationDto
    except Exception as exception:
        log.warning(log.warning, 'There is most likely an issue related to queue-manager-api dependencies imports', exception=exception)
        from notification_manager_api import NotificationConfig
        from notification_manager_api import NotificationSeverity
        from notification_manager_api import NotificationDestiny
        from notification_manager_api import NotificationConstant
        from notification_manager_api import NotificationDto


def buildNotificationService():

    @Service()
    class NotificationService:

        @ServiceMethod(requestClass=[str])
        def notifyTest(self, text):
            return self.logAndNotifyBySeverityTo([text], NotificationSeverity.TEST, NotificationConstant.DEFAULT_DESTINY_LIST_DTO)

        @ServiceMethod(requestClass=[str, [EnumItem]])
        def notifyTestTo(self, text, destinyList):
            return self.logAndNotifyBySeverityTo([text], NotificationSeverity.TEST, destinyList)

        @ServiceMethod(requestClass=[str])
        def notifyDebug(self, text):
            return self.logAndNotifyBySeverityTo([text], NotificationSeverity.DEBUG, NotificationConstant.DEFAULT_DESTINY_LIST_DTO)

        @ServiceMethod(requestClass=[str, [EnumItem]])
        def notifyDebugTo(self, text, destinyList):
            return self.logAndNotifyBySeverityTo([text], NotificationSeverity.DEBUG, destinyList)

        @ServiceMethod(requestClass=[str])
        def notifySetting(self, text):
            return self.logAndNotifyBySeverityTo([text], NotificationSeverity.SETTING, NotificationConstant.DEFAULT_DESTINY_LIST_DTO)

        @ServiceMethod(requestClass=[str, [EnumItem]])
        def notifySettingTo(self, text, destinyList):
            return self.logAndNotifyBySeverityTo([text], NotificationSeverity.SETTING, destinyList)

        @ServiceMethod(requestClass=[str])
        def notifyInfo(self, text):
            return self.logAndNotifyBySeverityTo([text], NotificationSeverity.INFO, NotificationConstant.DEFAULT_DESTINY_LIST_DTO)

        @ServiceMethod(requestClass=[str, [EnumItem]])
        def notifyInfoTo(self, text, destinyList):
            return self.logAndNotifyBySeverityTo([text], NotificationSeverity.INFO, destinyList)

        @ServiceMethod(requestClass=[str])
        def notifyStatus(self, text):
            return self.logAndNotifyBySeverityTo([text], NotificationSeverity.STATUS, NotificationConstant.DEFAULT_DESTINY_LIST_DTO)

        @ServiceMethod(requestClass=[str, [EnumItem]])
        def notifyStatusTo(self, text, destinyList):
            return self.logAndNotifyBySeverityTo([text], NotificationSeverity.STATUS, destinyList)

        @ServiceMethod(requestClass=[str])
        def notifyWarning(self, text):
            return self.logAndNotifyBySeverityTo([text], NotificationSeverity.WARNING, NotificationConstant.DEFAULT_DESTINY_LIST_DTO)

        @ServiceMethod(requestClass=[str, [EnumItem]])
        def notifyWarningTo(self, text, destinyList):
            return self.logAndNotifyBySeverityTo([text], NotificationSeverity.WARNING, destinyList)

        @ServiceMethod(requestClass=[str])
        def notifyFailure(self, text):
            return self.logAndNotifyBySeverityTo([text], NotificationSeverity.FAILURE, NotificationConstant.DEFAULT_DESTINY_LIST_DTO)

        @ServiceMethod(requestClass=[str, [EnumItem]])
        def notifyFailureTo(self, text, destinyList):
            return self.logAndNotifyBySeverityTo([text], NotificationSeverity.FAILURE, destinyList)

        @ServiceMethod(requestClass=[str])
        def notifySuccess(self, text):
            return self.logAndNotifyBySeverityTo([text], NotificationSeverity.SUCCESS, NotificationConstant.DEFAULT_DESTINY_LIST_DTO)

        @ServiceMethod(requestClass=[str, [EnumItem]])
        def notifySuccessTo(self, text, destinyList):
            return self.logAndNotifyBySeverityTo([text], NotificationSeverity.SUCCESS, destinyList)

        @ServiceMethod(requestClass=[str])
        def notifyError(self, text):
            return self.logAndNotifyBySeverityTo([text], NotificationSeverity.ERROR, NotificationConstant.DEFAULT_DESTINY_LIST_DTO)

        @ServiceMethod(requestClass=[str, [EnumItem]])
        def notifyErrorTo(self, text, destinyList):
            return self.logAndNotifyBySeverityTo([text], NotificationSeverity.ERROR, destinyList)

        @ServiceMethod(requestClass=[[str], EnumItem, [EnumItem]])
        def logAndNotifyBySeverityTo(self, textList, severity, destinyList):
            for text in textList:
                log.log(
                    self.logAndNotifyBySeverityTo,
                    text,
                    exception = None,
                    muteStackTrace = True,
                    newLine = False,
                    level = severity.logLevel
                )
            return self.notifyAll([
                NotificationDto.NotificationRequestDto(
                    message = str(text),
                    severity = severity,
                    destinyList = destinyList
                )
                for text in textList
            ])


        @ServiceMethod(requestClass=[[NotificationDto.NotificationRequestDto]])
        def notifyAll(self, dtoList):
            return self.notifyAllByApiKey(dtoList, NotificationConfig.NOTIFICATION_API_KEY)


        @ServiceMethod(requestClass=[[NotificationDto.NotificationRequestDto]])
        def notifyAllByCurrentApiKey(self, dtoList):
            currentApiKeyWithBearer = FlaskUtil.safellyGetHeaders().get(JwtConstant.DEFAULT_JWT_API_KEY_HEADER_NAME, c.BLANK)
            self.validator.notification.validateNotificationApiKey(currentApiKeyWithBearer)
            return self.notifyAllByApiKey(dtoList, currentApiKeyWithBearer.split()[-1])


        @ServiceMethod(requestClass=[[NotificationDto.NotificationRequestDto], str])
        def notifyAllByApiKey(self, dtoList, notificationApiKey):
            if ObjectHelper.isNone(notificationApiKey):
                return self.notifyAllByCurrentApiKey(dtoList)
            return self.emitter.notification.notifyAll(dtoList, notificationApiKey)

    return NotificationService
