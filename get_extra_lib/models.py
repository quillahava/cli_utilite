from pydantic import BaseModel
from typing import List
import json


class Package(BaseModel):
    name: str
    epoch: int | None = None
    version: str
    release: str
    arch: str | None = None
    disttag: str | None = None
    buildtime: int | None = None
    source: str | None = None


class PackageEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Package):
            return obj.model_dump()
        return json.JSONEncoder.default(self, obj)


class JsonResponse(BaseModel):
    request_args: dict
    length: int
    packages: List[Package]
