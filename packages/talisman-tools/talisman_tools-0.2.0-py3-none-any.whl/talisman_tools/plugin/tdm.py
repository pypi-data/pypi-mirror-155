from tdm.json_schema import TalismanDocumentModel

from .abstract import AbstractPluginManager


class TDMPluginManager(AbstractPluginManager):
    def __init__(self):
        AbstractPluginManager.__init__(self, 'TDM', TalismanDocumentModel)

    @staticmethod
    def _check_value(value) -> bool:
        return isinstance(value, type) and issubclass(value, TalismanDocumentModel)
