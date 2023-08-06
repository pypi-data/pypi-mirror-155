import json

from jsonpickle.pickler import Pickler

from json_cfdi.wrappers.cfdi33 import CFDI as CFDIv33
from json_cfdi.wrappers.cfdi40 import CFDI as CFDIv40
from json_cfdi.wrappers.schemas import get_schema


class CFDI:
    def __init__(self, file, version=3.3, context=None):
        self.file = file

        self.context = context
        self.version = version
        self.schema = get_schema(self.version, context=self.context)

        self._dict = None
        self._raw = None
        self._model = None
        self._json = None

        # variables auxiliares
        # para convertir dict > JSON
        self._pickler = Pickler(use_decimal=False)

    def to_raw(self):
        if self._raw:
            return self._raw
        self._raw = self.schema.to_dict(self.file)
        return self._raw

    def to_model(self):
        if self._model:
            return self._model
        if self.version == 3.3:
            self._model = CFDIv33(self.to_raw())
        elif self.version == 4.0:
            self._model = CFDIv40(self.to_raw())
        return self._model

    def to_dict(self):
        if self._dict:
            return self._dict
        self._dict = self._pickler.flatten(self.to_model())
        return self._dict

    def to_json(self):
        if self._json:
            return self._json
        self._json = json.dumps(self.to_dict())
        return self._json
