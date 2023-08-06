from python_helper import Constant as c
from python_helper import log, ObjectHelper, StringHelper


def getEnumAsSpeech(enum) :
    return getConstantNameAsSpeech(enum.enumName)


def getConstantNameAsSpeech(enumName) :
    serviceReturn = None
    try:
        serviceReturn = StringHelper.join(getConstantNameAsSpeechList(enumName), character=c.SPACE)
    except Exception as exception:
         log.warning(getConstantNameAsSpeech, 'Not possible to parse name as speech', exception=exception, muteStackTrace=True)
    return serviceReturn


def getConstantNameAsSpeechList(enumName) :
    serviceReturn = None
    try:
        serviceReturn = [] if ObjectHelper.isNone(enumName) else enumName.lower().split(c.UNDERSCORE)
    except Exception as exception:
         log.warning(getConstantNameAsSpeechList, 'Not possible to parse constant as speech list', exception=exception, muteStackTrace=True)
    return serviceReturn
