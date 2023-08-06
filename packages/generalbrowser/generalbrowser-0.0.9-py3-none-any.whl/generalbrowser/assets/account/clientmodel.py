
from generalbrowser.assets.base.clientmodel import GeneralClientModel
from generalbrowser.assets.account.clientpage import GeneralAccountPage


class AccountClientModel(GeneralClientModel):
    _page_cls = GeneralAccountPage

    def __init__(self, email):
        self.email = email
