from python_helper import log
from python_framework import Serializer

try:
    from enumeration.NotificationSeverity import NotificationSeverity
    from enumeration.NotificationStatus import NotificationStatus
    from enumeration.NotificationDestiny import NotificationDestiny
except:
    try:
        from notification_manager_api.api.src.enumeration.NotificationSeverity import NotificationSeverity
        from notification_manager_api.api.src.enumeration.NotificationStatus import NotificationStatus
        from notification_manager_api.api.src.enumeration.NotificationDestiny import NotificationDestiny
    except Exception as exception:
        log.warning(log.warning, 'There is most likely an issue related to queue-manager-api dependencies imports', exception=exception)
        from notification_manager_api import NotificationSeverity
        from notification_manager_api import NotificationStatus
        from notification_manager_api import NotificationDestiny


DEFAULT_MESSAGE = 'No message was sent'
DEFAULT_SEVERITY = NotificationSeverity.NONE
DEFAULT_STATUS = NotificationStatus.NONE
DEFAULT_DESTINY_LIST_DTO = [
    NotificationDestiny.TELEGRAM,
    NotificationDestiny.VOICE
]
DEFAULT_DESTINY_LIST_MODEL = Serializer.jsonifyIt(DEFAULT_DESTINY_LIST_DTO)
