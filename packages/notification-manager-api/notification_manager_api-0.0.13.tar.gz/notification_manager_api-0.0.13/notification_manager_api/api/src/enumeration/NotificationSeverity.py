from python_helper import log
from python_framework import Enum, EnumItem


@Enum()
class NotificationSeverityEnumeration :

    NONE = EnumItem(degree=-1, logLevel=log.LOG)

    TEST = EnumItem(degree=0, logLevel=log.TEST)

    DEBUG = EnumItem(degree=1, logLevel=log.DEBUG)
    SETTING = EnumItem(degree=2, logLevel=log.SETTING)
    INFO = EnumItem(degree=3, logLevel=log.INFO)
    STATUS = EnumItem(degree=4, logLevel=log.STATUS)

    WARNING = EnumItem(degree=5, logLevel=log.WARNING)
    FAILURE = EnumItem(degree=6, logLevel=log.FAILURE)
    SUCCESS = EnumItem(degree=7, logLevel=log.SUCCESS)
    ERROR = EnumItem(degree=8, logLevel=log.ERROR)

NotificationSeverity = NotificationSeverityEnumeration()
