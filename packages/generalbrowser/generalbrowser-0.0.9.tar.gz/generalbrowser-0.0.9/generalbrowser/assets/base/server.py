
from rest_framework.response import Response
from django.http import HttpResponse

from generalbrowser.assets.base.client_and_server import _GeneralClientAndServer
from generallibrary import getBaseClassNames, dumps, deco_optional_suppress


class GeneralServer(_GeneralClientAndServer):
    """ Server methods to talk to client. """
    _token = ...
    _account_cls = ...

    def __init__(self):
        assert self._token is not Ellipsis
        assert "APIView" in getBaseClassNames(self)  # from rest_framework.views import APIView

    @deco_optional_suppress(Exception, return_bool=False)
    def account(self, error=True):
        """ Return account or None if error is False. """
        # Raise HttpResponse? If not signed in
        return self._account_cls.objects.get(pk=self.session("account_pk"))

    def signin(self, account):
        self.session(account_pk=account.pk)

    def signout(self):
        self.session(account_pk=None)


    def auth_token(self):
        """ Authorize token for server-to-server. """
        assert self._token is not Ellipsis
        token, = self.extract_data("token")
        if token != self._token:
            self.fail("Invalid token")

    def session(self, arg=None, **kwargs):
        """ Set session values with kwargs and return session values with args.

            :param rest_framework.views.APIView or GeneralServer self:
            :param arg: Optional key arg to return session value of. """
        for key, value in kwargs.items():
            self.request.session[key] = value
        if arg is not None:
            return self.request.session[arg]

    @property
    def data(self):
        """ Dictionary of POST values.

            :param rest_framework.views.APIView or GeneralServer self: """
        return self.request.POST.dict()

    def extract_data(self, *keys, default=...):
        """ Returns tuple with values of given keys, error for missing keys unless default is specified. """
        if default is Ellipsis:
            return tuple(self.data[key] for key in keys)
        else:
            return tuple(self.data.get(key, default) for key in keys)

    @staticmethod
    def serialize(*models):
        """ Todo: Send client models in header instead? That way we can serialize inside success method instead.
            Convert django models to client models. """
        client_models = [model.create_client_model() for model in models]
        return HttpResponse(dumps(client_models), headers={"testing": 5})
        # return HttpResponse(dumps(client_models), content_type="application/octet-stream", headers={"testing": 5})

    @staticmethod
    def success(msg=None, files=None, code=None):
        if files:
            filename, file = next(iter(files.items()))
            response = HttpResponse(file, content_type="application/octet-stream")
            response["Content-Disposition"] = f'attachment; filename={filename}'
        else:
            response = Response(msg)
        if code is not None:
            response.status_code = code
        return response

