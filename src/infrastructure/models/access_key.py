from pydantic import BaseModel

class AccessKeyDto(BaseModel):

    id_: str
    user_id: str
    created_at: str
    expire_at: str
