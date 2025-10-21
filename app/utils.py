import hashlib
from typing import Dict, Any, List
from datetime import datetime
import re



def sha256_hash(s: str) -> str:
    return hashlib.sha256(s.encode('utf-8')).hexdigest()

def get_length(s: str) -> int:
    return len(s)

def is_palindrome(s: str) -> bool:
    cleaned = ''.join(ch.lower() for ch in s if not ch.isspace())
    return cleaned == cleaned[::-1]

def unique_characters(s: str) -> int:
    return len(set(s))

def count_words(s: str) -> int:
  
    words = re.findall(r'\S+', s)
    return len(words)

def char_frequency_map(s: str) -> Dict[str, int]:
    freq: Dict[str, int] = {}
    for ch in s:
        freq[ch] = freq.get(ch, 0) + 1
    return freq

def filter_strings(db: Dict[str, Dict], filters: Dict[str, Any]) -> List[Dict]:
    """
    db structure:
      key: sha256_hash
      value: {"id": sha256, "value": original_value, "properties": {...}, "created_at": datetime}
    filters may include:
      - is_palindrome (bool)
      - min_length (int)
      - max_length (int)
      - word_count (int)
      - contains_character (str)
    Returns list of dicts matching the spec shape (id, value, properties, created_at)
    """
    results = []
    for item in db.values():
        props = item["properties"]
        ok = True

        if "is_palindrome" in filters:
            if props.get("is_palindrome") != filters["is_palindrome"]:
                ok = False

        if "min_length" in filters:
            if props.get("length", 0) < int(filters["min_length"]):
                ok = False

        if "max_length" in filters:
            if props.get("length", 0) > int(filters["max_length"]):
                ok = False

        if "word_count" in filters:
            if props.get("word_count") != int(filters["word_count"]):
                ok = False

        if "contains_character" in filters:
            ch = filters["contains_character"]
            if not isinstance(ch, str) or len(ch) == 0:
                ok = False
            else:
          
                if ch not in item["value"]:
                    ok = False

        if ok:
            results.append({
                "id": item["id"],
                "value": item["value"],
                "properties": props,
                "created_at": item["created_at"]
            })
    return results


def parse_natural_language_query(query: str) -> Dict[str, Any]:
    """
    Supports simple phrases:
      - "all single word palindromic strings" -> {"word_count": 1, "is_palindrome": True}
      - "strings longer than 10 characters" -> {"min_length": 11}
      - "strings containing the letter z" -> {"contains_character": "z"}
      - "palindromic strings that contain the first vowel" -> is_palindrome + contains_character=a (heuristic)
    Raises ValueError if unable to parse.
    """
    q = query.lower().strip()
    filters = {}


    if re.search(r'\bsingle word\b', q) or re.search(r'\bone word\b', q):
        filters["word_count"] = 1

 
    if 'palindrom' in q:
        filters["is_palindrome"] = True


    m = re.search(r'longer than (\d+)', q)
    if m:
        n = int(m.group(1))
        filters["min_length"] = n + 1

    m2 = re.search(r'longer than (\d+)\s*characters', q)
    if m2:
        n = int(m2.group(1))
        filters["min_length"] = n + 1

    m3 = re.search(r'containing (?:the )?letter ([a-z])', q)
    if m3:
        filters["contains_character"] = m3.group(1)

 
    m4 = re.search(r'containing the letter (\w)', q)
    if m4:
        filters["contains_character"] = m4.group(1)

    m5 = re.search(r'containing (\w)', q)
    if m5 and "contains_character" not in filters:
      
        ch = m5.group(1)
        if len(ch) == 1:
            filters["contains_character"] = ch

    if 'first vowel' in q:
   
        filters["contains_character"] = 'a'
        filters["is_palindrome"] = True

    if not filters:
        raise ValueError("Could not interpret query")

    return filters
