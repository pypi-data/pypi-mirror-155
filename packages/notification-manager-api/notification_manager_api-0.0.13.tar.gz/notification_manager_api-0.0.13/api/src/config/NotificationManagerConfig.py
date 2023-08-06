from globals import getGlobalsInstance
globalsInstance = getGlobalsInstance()

from constant import NotificationConfigurationKeyConstant


CURRENT_NOTIFICARION_DEGREE = globalsInstance.getSetting(NotificationConfigurationKeyConstant.CURRENT_NOTIFICARION_DEGREE)
