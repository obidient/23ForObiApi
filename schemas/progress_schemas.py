import pydantic as pd


class ProgressSchemaBase(pd.BaseModel):
    id: str
    number_of_voters: int
    total_number_of_voters_expected: int
    progress_percentage: int

    class Config:
        orm_mode = True
