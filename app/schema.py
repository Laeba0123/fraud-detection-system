from pydantic import BaseModel, Field
from typing import List

class Transaction(BaseModel):
    features: List[float] = Field(description="List of transaction features")

    class Config:
     json_schema_extra = {
        "example": {
            "features": [0.1] * 30
        }
    }