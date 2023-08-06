from python_framework import ResourceManager
from queue_manager_api import QueueManager

import ModelAssociation
from manager.NotificationManager import NotificationManager


app = ResourceManager.initialize(__name__, ModelAssociation.MODEL, managerList=[
    QueueManager(),
    NotificationManager()
])
