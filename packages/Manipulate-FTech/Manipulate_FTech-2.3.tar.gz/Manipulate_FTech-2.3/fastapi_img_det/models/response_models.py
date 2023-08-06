from pydantic import BaseModel


class Output(BaseModel):
    result: str

