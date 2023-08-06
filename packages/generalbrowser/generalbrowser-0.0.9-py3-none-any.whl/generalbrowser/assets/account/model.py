
from django.db import models

from generalbrowser.assets.base.model import GeneralModel
from generalbrowser.assets.account.clientmodel import AccountClientModel


class GeneralAccountModel(GeneralModel):
    _client_model_cls = AccountClientModel

    email = models.EmailField()
    password = models.CharField(max_length=100)

    class Meta:
        abstract = True

    def hash_password(self): ...

    def __str__(self):
        return self.email



