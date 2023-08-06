
from generalgui import Page


class GeneralClientPage(Page):
    """ All pages (parts even?) in a browser gui should inherit this.
        Make sure to include client as parameter if this client page is created as the first page. """
    def __init__(self, client=None, parent=None):
        self.client = getattr(self.get_parent(), "client", client)
        assert self.client
        self.client.debug = True  # Render failed responses

        self.mainpage = getattr(self.get_parent(), "mainpage", None) or self


class GeneralModelPage(GeneralClientPage):
    """ All pages that display a specific model should inherit this. """
    def __init__(self, model=None, parent=None):
        self.model = model

