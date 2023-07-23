from pydantic import BaseModel
from typing import List


class Package(BaseModel):
    name: str
    epoch: int
    version: str
    release: str
    arch: str
    disttag: str
    buildtime: int
    source: str


class JsonResponse(BaseModel):
    request_args: dict
    length: int
    packages: List[Package]
