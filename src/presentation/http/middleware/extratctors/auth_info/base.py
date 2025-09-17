from starlette.requests import Request
from abc import abstractmethod
from presentation.models import AuthInfo
from typing import Protocol


class AuthInfoExtractor(Protocol):

    @abstractmethod
    async def __call__(self, request: Request) -> AuthInfo | None:
        raise NotImplementedError



        

