from python_framework import Enum, EnumItem


@Enum()
class NotificationDestinyEnumeration :

    TELEGRAM = EnumItem()
    EMAIL = EnumItem()
    VOICE = EnumItem()

NotificationDestiny = NotificationDestinyEnumeration()
