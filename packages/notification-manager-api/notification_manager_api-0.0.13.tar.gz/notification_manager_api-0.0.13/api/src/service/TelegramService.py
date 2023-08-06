from python_helper import ObjectHelper
from python_framework import Service, ServiceMethod


@Service()
class TelegramService:

    @ServiceMethod(requestClass=[[str]])
    def messageAll(self, textList):
        serviceReturn = None
        if ObjectHelper.isNotEmpty(textList):
            try:
                serviceReturn = self.emitter.telegram.messageAll([{"message": text} for text in textList])
            except Exception as exception:
                log.failure(self.messageAll, 'Not possible to speak all', exception=exception, muteStackTrace=True)
        return serviceReturn


    @ServiceMethod(requestClass=[str])
    def message(self, text):
        serviceReturn = None
        try:
            serviceReturn = self.messageAll([text])
        except Exception as exception:
            log.failure(self.message, 'Not possible to speak', exception=exception, muteStackTrace=True)
        return serviceReturn
