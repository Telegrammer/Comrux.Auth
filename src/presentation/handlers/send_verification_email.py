__all__ = ["SendEmailVerificationHandler"]

from application.usecases import SendEmailVerificationRequest, SendEmailVerificationLinkUsecase
from application.ports import UnitOfWork


class SendEmailVerificationHandler:

    def __init__(self, usecase: SendEmailVerificationLinkUsecase, unit_of_work: UnitOfWork):
        self._usecase = usecase
        self._unit_of_work = unit_of_work

    async def __call__(self, user_id: str):
        async with self._unit_of_work:
            await self._usecase(SendEmailVerificationRequest.from_primitives(user_id))