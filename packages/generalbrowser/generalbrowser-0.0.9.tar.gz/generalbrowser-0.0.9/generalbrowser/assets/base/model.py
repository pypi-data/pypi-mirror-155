
from django.db import models

from generallibrary import SigInfo, getBaseClassNames


class GeneralModel(models.Model):
    """ Server model methods. """
    class Meta:
        abstract = True

    _client_model_cls = ...

    # def __init__(self):  # Not sure if init is ever called
    #     assert "Model" in getBaseClassNames(self)  # from django.db.models import Model

    def create_client_model(self):
        """ Create a client model class for server models attributes.
            Recursively creates ClientModels for attrs that might be another model. """
        kwargs = {}
        for name in SigInfo(self._client_model_cls.__init__).names:
            if name == "self":
                continue
            attr = getattr(self, name)
            if isinstance(attr, GeneralModel):
                attr = attr.create_client_model()
            kwargs[name] = attr

        return self._client_model_cls(**kwargs)

