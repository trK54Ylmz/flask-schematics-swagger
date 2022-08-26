from json import JSONEncoder
from typing import Any

from schematics import Model
from schematics.common import NONEMPTY


class CustomEncoder(JSONEncoder):
    def default(self, o: Any) -> Any:
        """
        Serialize custom objects

        :param o: data object
        :return: serialized value
        """
        if isinstance(o, Model):
            return o.to_native(export_level=NONEMPTY)
        return super().default(o)
