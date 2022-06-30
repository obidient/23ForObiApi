from pydantic import BaseModel

class TestSchema(BaseModel):
    text: str

    class Config:
        orm_mode = True

