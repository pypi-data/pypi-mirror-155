from python_framework import SqlAlchemyProxy as sap
from python_framework import AuditoryUtil, AuditoryConstant

from constant import NotificationConstant
from ModelAssociation import MODEL, NOTIFICATION
from converter.static import NotificationStaticConverter


class Notification(MODEL):
    __tablename__ = NOTIFICATION

    id = sap.Column(sap.Integer(), sap.Sequence(f'{__tablename__}{sap.ID}{sap.SEQ}'), primary_key=True)
    message = sap.Column(sap.String(sap.STRING_SIZE), nullable=False, default=NotificationConstant.DEFAULT_MESSAGE)
    severity = sap.Column(sap.String(sap.LITTLE_STRING_SIZE), nullable=False, default=NotificationConstant.DEFAULT_SEVERITY)
    destinyList = sap.Column(sap.String(sap.STRING_SIZE), nullable=False, default=str(NotificationConstant.DEFAULT_DESTINY_LIST_MODEL))
    status = sap.Column(sap.String(sap.LITTLE_STRING_SIZE), nullable=False, default=NotificationConstant.DEFAULT_STATUS)
    createdAt = sap.Column(sap.DateTime(), nullable=False)
    updatedAt = sap.Column(sap.DateTime(), nullable=False)
    createdBy = sap.Column(sap.String(sap.MEDIUM_STRING_SIZE), nullable=False, default=AuditoryConstant.DEFAULT_USER)
    updatedBy = sap.Column(sap.String(sap.MEDIUM_STRING_SIZE), nullable=False, default=AuditoryConstant.DEFAULT_USER)

    def __init__(self,
        id = None,
        message = None,
        severity = None,
        destinyList = None,
        status = None,
        createdAt = None,
        updatedAt = None,
        createdBy = None,
        updatedBy = None
    ):
        self.id = id
        self.message = NotificationStaticConverter.toMessage(message)
        self.severity = NotificationStaticConverter.toSeverity(severity)
        self.destinyList = NotificationStaticConverter.toDestinyListModel(destinyList)
        self.status = NotificationStaticConverter.toStatus(status)
        self.createdAt = createdAt
        self.updatedAt = updatedAt
        self.createdBy = createdBy
        self.updatedBy = updatedBy
        AuditoryUtil.overrideApiKeyData(self)

    def getDestinyList(self):
        # destinyList = NotificationStaticConverter.toDestinyListDto(self.destinyList)
        # print(destinyList)
        return NotificationStaticConverter.toDestinyListDto(self.destinyList)

    def __repr__(self):
        return f'{self.__tablename__}(id: {self.id}, severity: {self.severity}, destinyList: {self.destinyList} status: {self.status})'
