from pydantic import BaseModel, model_validator
from typing import Optional
from datetime import datetime


class StoryOut(BaseModel):
    id: int
    title: Optional[str]
    score: Optional[int]
    url: Optional[str]
    author: Optional[str]
    time: Optional[int]
    descendants: Optional[int]
    type: Optional[str]
    readable_time: Optional[str] = None  # Add this field explicitly

    @model_validator(mode='before')
    def convert_timestamp_to_readable_time(cls, self):
        # Convert UNIX timestamp to human-readable format before returning the data
        if self.time:
            self.readable_time = datetime.fromtimestamp(self.time).strftime("%Y-%m-%d %H:%M:%S")
        return self
        
    class Config:
        from_attributes = True # Enable from_attributes to allow using attributes directly
