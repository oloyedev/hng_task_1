from pydantic import BaseModel
from datetime import datetime
from typing import Dict, Optional, List, Any

class CreateString(BaseModel):
    value: str

class StringProperties(BaseModel):
    length: int
    is_palindrome: bool
    unique_characters: int
    word_count: int
    sha256_hash: str
    character_frequency_map: Dict[str, int]

class StringResponse(BaseModel):
    id: str
    value: str
    properties: StringProperties
    created_at: datetime

class FilterResponse(BaseModel):
    data: List[StringResponse]
    count: int
    filters_applied: Dict[str, Optional[Any]]

class NaturalLanguageResponse(BaseModel):
    data: List[StringResponse]
    count: int
    interpreted_query: Dict[str, Any]
