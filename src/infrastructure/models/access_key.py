from pydantic import BaseModel

class AccessKey(BaseModel):

    id_: str
    user_id: str
    created_at: str
    expire_at: str
