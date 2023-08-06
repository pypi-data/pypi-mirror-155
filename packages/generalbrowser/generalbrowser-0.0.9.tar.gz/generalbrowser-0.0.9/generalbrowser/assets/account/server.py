
from generalbrowser.assets.base.server import GeneralServer


class GeneralAccountServer(GeneralServer):
    """ Register new account.
        Sign in.
        Sign out.
        See if signed in. """

    def _get_email_and_pass(self):
        email, password = self.extract_data("email", "password", default=None)
        if email is None or password is None:
            return None, None

        self.scrub_email(email)
        self.scrub_password(password)
        return email, password

    def post(self, _):
        email, password = self._get_email_and_pass()

        if email is None or password is None:
            self.signout()
            return self.success("Signed out")

        if self._account_cls.objects.filter(email__exact=email):
            self.fail("An account with that email already exists")

        account = self._account_cls(email=email, password=password)
        account.save()
        self.signin(account=account)

        return self.success("Registered")

    def get(self, _):
        email, password = self._get_email_and_pass()

        if email is None or password is None:
            account = self.account(error=False)
            if account is None:
                return self.success("Not signed in", code=204)
            else:
                return self.serialize(account)  # These two should return same thing

        account = self._account_cls.objects.filter(email__exact=email, password__exact=password)
        if not account:
            return self.fail("No account with those credentials")
        account = account[0]

        self.signin(account=account)
        return self.serialize(account)  # These two should return same thing



