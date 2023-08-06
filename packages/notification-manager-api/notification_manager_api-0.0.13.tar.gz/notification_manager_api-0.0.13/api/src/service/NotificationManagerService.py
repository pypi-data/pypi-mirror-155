from python_helper import Constant as c
from python_helper import log, ObjectHelper, StringHelper
from python_framework import Service, ServiceMethod, EnumItem, AuditoryUtil

from config import NotificationManagerConfig
from enumeration.NotificationSeverity import NotificationSeverity
from enumeration.NotificationStatus import NotificationStatus
from enumeration.NotificationDestiny import NotificationDestiny
import NotificationDto
import Notification


# def isValid(destiny, model):
#     result = destiny in model.getDestinyList()
#     print(f'{destiny} in {model.getDestinyList()}: {result}')
#     return result



@Service()
class NotificationManagerService:

    destinyServices = {}

    @ServiceMethod(requestClass=[[Notification.Notification]])
    def notifyAll(self, modelList):
        serviceException = None
        nextModelStatus = None
        filteredModelList = [
            model
            for model in modelList
            if NotificationManagerConfig.CURRENT_NOTIFICARION_DEGREE <= NotificationSeverity.map(model.severity).degree
        ]
        try:
            nodificationResponses = [
                self.getDestinyService(destiny)([
                    f'{model.severity} from {StringHelper.join(StringHelper.join(model.createdBy.split(c.DASH), character=c.SPACE).split(c.DOT), character=c.SPACE)}: {model.message}'
                    for model in filteredModelList
                    if destiny in model.getDestinyList()
                ])
                for destiny in self.getDestinyServices()
            ]
            # nodificationResponses = []
            # for destiny in self.getDestinyServices():
            #     messageList = []
            #     for model in filteredModelList:
            #         if isValid(destiny, model):
            #             messageList.append(f'{model.severity} from {StringHelper.join(StringHelper.join(model.createdBy.split(c.DASH), character=c.SPACE).split(c.DOT), character=c.SPACE)}: {model.message}')
            #     nodificationResponses.append(self.getDestinyService(destiny)(messageList))
            nextModelStatus = NotificationStatus.DELIVERED
        except Exception as exception:
            serviceException = exception
            nextModelStatus = NotificationStatus.NOT_DELIVERED
            log.prettyPython(self.notifyAll, 'Not possible to deliver notifications', modelList, logLevel=log.FAILURE)
        self.mapper.notificationManager.overrideModelListStatus(modelList, nextModelStatus)
        self.persistAll(modelList)
        if ObjectHelper.isNotNone(serviceException):
            raise serviceException
        return nodificationResponses


    @ServiceMethod(requestClass=[[NotificationDto.NotificationRequestDto]])
    def acceptAll(self, dtoList):
        modelList = self.persistAll(self.mapper.notificationManager.fromRequestDtoListToModelList(dtoList))
        log.status(self.acceptAll, f'Accpeting notifications: {modelList}')
        return self.notifyAll(modelList)


    @ServiceMethod(requestClass=[[Notification.Notification]])
    def persistAll(self, modelList):
        log.status(self.persistAll, f'Persisting notifications: {modelList}')
        return self.repository.notificationManager.saveAll(modelList)


    @ServiceMethod()
    def getDestinyServices(self):
        if ObjectHelper.isEmpty(self.destinyServices):
            self.destinyServices[NotificationDestiny.TELEGRAM] = self.service.telegram.messageAll
            self.destinyServices[NotificationDestiny.VOICE] = self.service.voice.speakAll
            self.destinyServices[NotificationDestiny.EMAIL] = self.service.email.emailAll
        return self.destinyServices


    @ServiceMethod(requestClass=[EnumItem])
    def getDestinyService(self, destiny):
        # result = self.getDestinyServices().get(destiny)
        # print(result)
        return self.getDestinyServices().get(destiny)
