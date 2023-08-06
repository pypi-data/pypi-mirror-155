
import json

from generallibrary import SigInfo, AutoInitBases


class GeneralClientModel(metaclass=AutoInitBases):
    _page_cls = ...

    def __repr__(self):
        attrs = {name: getattr(self, name) for name in SigInfo(type(self).__init__).names if name != "self"}
        return f"<{type(self).__name__}: {attrs}>"

    def create_page(self, parent=None):
        return self._page_cls(model=self, parent=parent)
