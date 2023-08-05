from pydantic import BaseModel
from typing import List, Union
import json


class Package(BaseModel):
    name: str
    epoch: Union[int, None] = None
    version: str
    release: str
    arch: Union[str, None] = None
    disttag: Union[str, None] = None
    buildtime: Union[int, None] = None
    source: Union[str, None] = None


class PackageEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Package):
            return obj.dict()
        return super().default(obj)


class JsonResponse(BaseModel):
    request_args: dict
    length: int
    packages: List[Package]
