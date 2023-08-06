from python_framework import Mapper, MapperMethod, EnumItem, AuditoryUtil

from enumeration.NotificationStatus import NotificationStatus
import Notification
import NotificationDto


RECEIVED_STATUS = NotificationStatus.RECEIVED


@Mapper()
class NotificationManagerMapper:

    @MapperMethod(requestClass=[[NotificationDto.NotificationRequestDto]], responseClass=[[Notification.Notification]])
    def fromRequestDtoListToModelList(self, dtoList, modelList):
        self.overrideModelListStatus(modelList, RECEIVED_STATUS)
        return modelList


    @MapperMethod(requestClass=[[Notification.Notification]], responseClass=[[NotificationDto.NotificationResponseDto]])
    def fromModelListToResponseDtoList(self, modelList, dtoList):
        return dtoList


    @MapperMethod(requestClass=[NotificationDto.NotificationRequestDto], responseClass=[Notification.Notification])
    def fromRequestDtoToModel(self, dto, model):
        self.overrideModelStatus(model, RECEIVED_STATUS)
        return model


    @MapperMethod(requestClass=[Notification.Notification], responseClass=[NotificationDto.NotificationResponseDto])
    def fromModelToResponseDto(self, model, dto):
        return dto

    @MapperMethod(requestClass=[[Notification.Notification], EnumItem])
    def overrideModelListStatus(self, modelList, status):
        for model in modelList:
            self.overrideModelStatus(model, status)
        return modelList


    @MapperMethod(requestClass=[Notification.Notification, EnumItem])
    def overrideModelStatus(self, model, status):
        model.status = status
        AuditoryUtil.overrideApiKeyData(model)
        return model
