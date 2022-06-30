
from pydantic import BaseModel, UUID4



class Response(BaseModel):
    code: int
    message: str