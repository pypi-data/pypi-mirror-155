import inspect
from base64 import b64encode

from pydantic import BaseModel


class Base(BaseModel):
    @classmethod
    def from_telegram_type_dict(cls, obj) -> dict:
        cls_dict = {}
        if 'owner_id' in cls.__fields__:
            cls_dict['owner_id'] = obj._client.cached_me.id
        for a, v in obj.__dict__.items():
            if a not in cls.__fields__:
                continue
            field_type = cls.__fields__[a].type_
            if type(v) == bytes:
                v = b64encode(v).decode()
            cls_dict[a] = ( field_type.from_telegram_type(v)
                            if inspect.isclass(field_type) and issubclass(field_type, Base)
                            else v )
        return cls_dict

    @classmethod
    def from_telegram_type(cls, obj):
        if obj is None:
            return None
        if isinstance(obj, list):
            return [cls.from_telegram_type(o) for o in obj]
        return cls(**cls.from_telegram_type_dict(obj))
