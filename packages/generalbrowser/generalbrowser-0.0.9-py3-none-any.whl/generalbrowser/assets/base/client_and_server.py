
from re import fullmatch
from rest_framework.exceptions import ValidationError

from generallibrary import BoolStr, AutoInitBases, deco_optional_suppress



class _GeneralClientAndServer(metaclass=AutoInitBases):
    _error = ValidationError

    def fail(self, msg=None):
        # return Response(f"Fail: {msg}")
        raise self._error(msg)

    """ Inherited by GeneralServer & GeneralClient. """
    @staticmethod
    def _validate_email(email):
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if not fullmatch(regex, email):
            return BoolStr(False, "Invalid email")
        return BoolStr(True, "Valid email")

    @staticmethod
    def _validate_password(password):
        if len(password) < 8:
            return BoolStr(False, "Password has to be at least 8 characters.")
        return BoolStr(True, "Valid password")

    @deco_optional_suppress(_error)
    def _scrub(self, value, error, method):
        """ Raise ValidationError if not passing. """
        validation = method(value)
        if not validation:
            self.fail(msg=validation)
        return validation

    def scrub_email(self, email, error=True):
        return self._scrub(value=email, error=error, method=self._validate_email)

    def scrub_password(self, password, error=True):
        return self._scrub(value=password, error=error, method=self._validate_password)











