from python_helper import log
from python_framework import StaticConverter, Serializer

try:
    from enumeration.NotificationSeverity import NotificationSeverity
    from enumeration.NotificationStatus import NotificationStatus
    from enumeration.NotificationDestiny import NotificationDestiny
    from constant import NotificationConstant
except:
    try:
        from notification_manager_api.api.src.enumeration.NotificationSeverity import NotificationSeverity
        from notification_manager_api.api.src.enumeration.NotificationStatus import NotificationStatus
        from notification_manager_api.api.src.enumeration.NotificationDestiny import NotificationDestiny
        from notification_manager_api.api.src.constant import NotificationConstant
    except Exception as exception:
        log.warning(log.warning, 'There is most likely an issue related to queue-manager-api dependencies imports', exception=exception)
        from notification_manager_api import NotificationSeverity
        from notification_manager_api import NotificationStatus
        from notification_manager_api import NotificationDestiny
        from notification_manager_api import NotificationConstant


def toMessage(message):
    return StaticConverter.getValueOrDefault(
        message,
        NotificationConstant.DEFAULT_MESSAGE
    )


def toSeverity(severity):
    return NotificationSeverity.map(StaticConverter.getValueOrDefault(
        severity,
        NotificationConstant.DEFAULT_SEVERITY
    ))


def toDestinyListDto(destinyList):
    if isinstance(destinyList, str):
        destinyList = Serializer.convertFromJsonToDictionary(destinyList)
    return [
        NotificationDestiny.map(destiny)
        for destiny in StaticConverter.getValueOrDefault(
            destinyList,
            NotificationConstant.DEFAULT_DESTINY_LIST_DTO
        )
    ]


def toDestinyListModel(destinyList):
    return Serializer.jsonifyIt(destinyList)


def toStatus(status):
     return NotificationStatus.map(StaticConverter.getValueOrDefault(
        status,
        NotificationConstant.DEFAULT_STATUS
    ))
