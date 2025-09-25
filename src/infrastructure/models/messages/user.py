__all__ = ["UserSensetiveDataChange"]


from pydantic import BaseModel
from datetime import datetime


class UserSensetiveDataChange(BaseModel):
    user_id: str
    changed_fields: list[str]
    occured: datetime
