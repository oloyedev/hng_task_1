from fastapi import APIRouter, HTTPException, status, Query
from typing import Optional, Dict, Any, List
from. import schemas
from datetime import datetime
from .utils import (
    sha256_hash,
    get_length,
    is_palindrome,
    unique_characters,
    count_words,
    char_frequency_map,
    filter_strings,
    parse_natural_language_query
)

router = APIRouter()

db: Dict[str, Dict[str, Any]] = {}

@router.post('/strings', status_code=status.HTTP_201_CREATED, response_model=schemas.StringResponse)
def create_string(payload: schemas.CreateString):
    string_value = payload.value

    if string_value is None or (isinstance(string_value, str) and string_value.strip() == ""):
        raise HTTPException(status_code=400, detail="Invalid request body: 'value' cannot be empty")

    if not isinstance(string_value, str):
        raise HTTPException(status_code=422, detail="Invalid data type for 'value' (must be a string)")

    hashed_id = sha256_hash(string_value)

    if hashed_id in db:
        raise HTTPException(status_code=409, detail="String already exists in the system")

    props = {
        "length": get_length(string_value),
        "is_palindrome": is_palindrome(string_value),
        "unique_characters": unique_characters(string_value),
        "word_count": count_words(string_value),
        "sha256_hash": hashed_id,
        "character_frequency_map": char_frequency_map(string_value)
    }

    created_at = datetime.utcnow()

    db[hashed_id] = {
        "id": hashed_id,
        "value": string_value,
        "properties": props,
        "created_at": created_at
    }

    return {
        "id": hashed_id,
        "value": string_value,
        "properties": props,
        "created_at": created_at
    }


@router.get('/strings/filter-by-natural-language', response_model=schemas.NaturalLanguageResponse)
def filter_by_natural_language(query: str):
    try:
        parsed = parse_natural_language_query(query)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Unable to parse natural language query: {str(e)}")

    result = filter_strings(db, parsed)

    interpreted = {
        "original": query,
        "parsed_filters": parsed
    }

    return {
        "data": result,
        "count": len(result),
        "interpreted_query": interpreted
    }

@router.get('/strings/{string_value}', response_model=schemas.StringResponse)
def get_by_string_value(string_value: str):
    hashed_id = sha256_hash(string_value)
    if hashed_id not in db:
        raise HTTPException(status_code=404, detail="String does not exist in the system")

    item = db[hashed_id]
    return {
        "id": item["id"],
        "value": item["value"],
        "properties": item["properties"],
        "created_at": item["created_at"]
    }

@router.get('/strings', response_model=schemas.FilterResponse)
def get_all_strings(
    is_palindrome: Optional[bool] = Query(None),
    min_length: Optional[int] = Query(None),
    max_length: Optional[int] = Query(None),
    word_count: Optional[int] = Query(None),
    contains_character: Optional[str] = Query(None)
):
    filters: Dict[str, Any] = {}
    if is_palindrome is not None:
        filters["is_palindrome"] = is_palindrome
    if min_length is not None:
        filters["min_length"] = min_length
    if max_length is not None:
        filters["max_length"] = max_length
    if word_count is not None:
        filters["word_count"] = word_count
    if contains_character:
        if len(contains_character) != 1:
            raise HTTPException(status_code=400, detail="contains_character must be a single character")
        filters["contains_character"] = contains_character

    result = filter_strings(db, filters)

    return {
        "data": result,
        "count": len(result),
        "filters_applied": filters
    }


@router.delete('/strings/{string_value}', status_code=status.HTTP_204_NO_CONTENT)
def delete_string(string_value: str):
    hashed_id = sha256_hash(string_value)
    if hashed_id not in db:
        raise HTTPException(status_code=404, detail="String does not exist in the system")

    del db[hashed_id]
 
    return None
