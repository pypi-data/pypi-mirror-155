from python_helper import log
from globals import getGlobalsInstance
globalsInstance = getGlobalsInstance()

try:
    from constant import NotificationConfigurationKeyConstant
except:
    try:
        from notification_manager_api.api.src.constant import NotificationConfigurationKeyConstant
    except Exception as exception:
        log.warning(log.warning, 'There is most likely an issue related to queue-manager-api dependencies imports', exception=exception)
        from notification_manager_api import NotificationConfigurationKeyConstant


QUEUE_KEY = globalsInstance.getSetting(NotificationConfigurationKeyConstant.QUEUE_KEY)

EMITTER_API_KEY = globalsInstance.getSetting(NotificationConfigurationKeyConstant.EMITTER_API_KEY)
EMITTER_BASE_URL = globalsInstance.getSetting(NotificationConfigurationKeyConstant.EMITTER_BASE_URL)
EMITTER_TIMEOUT = globalsInstance.getSetting(NotificationConfigurationKeyConstant.EMITTER_TIMEOUT)

NOTIFICATION_API_KEY = globalsInstance.getSetting(NotificationConfigurationKeyConstant.NOTIFICATION_API_KEY)
