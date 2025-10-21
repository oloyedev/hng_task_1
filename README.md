# 🧩 String Analyzer Service — Backend Wizards Stage 1

A RESTful API service that analyzes strings, computes their properties, and supports both structured and natural-language filtering.

---

## 🚀 Overview

For each analyzed string, the service computes and stores:

| Property | Description |
|-----------|--------------|
| `length` | Number of characters in the string |
| `is_palindrome` | True if the string reads the same forwards and backwards (case-insensitive) |
| `unique_characters` | Count of distinct characters |
| `word_count` | Number of words separated by whitespace |
| `sha256_hash` | Unique SHA-256 hash of the string |
| `character_frequency_map` | Dictionary mapping each character to its occurrence count |

All strings are stored in memory (dictionary) for this stage, but the structure supports database integration (e.g., PostgreSQL) for persistence.

---

## 🧱 Tech Stack

- **Language:** Python 3.11+
- **Framework:** FastAPI
- **Server:** Uvicorn (ASGI)
- **Schema Validation:** Pydantic
- **Deployment (recommended):** Railway / Heroku / AWS / PXXL App

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository
``` bash
git clone https://github.com/<your-username>/string-analyzer-service.git
cd string-analyzer-service/app
```

### 2️⃣ Create Virtual Environment
``` bash
python -m venv venv
venv\Scripts\activate      # Windows
# source venv/bin/activate  # macOS/Linux
```

### 3️⃣ Install Dependencies
``` bash
pip install -r requirements.txt
```
### 4️⃣ Run Locally
From the project root:

``` bash
uvicorn app.main:app --reload
```
Server will start at:
👉 http://127.0.0.1:8000

Swagger Docs: http://127.0.0.1:8000/docs

### 🧠 API Endpoints

## 🔹 1. Create & Analyze String
POST /strings

``` JAON
{
  "value": "racecar"
}
```

Response 201

```JSON
{
  "id": "sha256_hash_value",
  "value": "racecar",
  "properties": {
    "length": 7,
    "is_palindrome": true,
    "unique_characters": 5,
    "word_count": 1,
    "sha256_hash": "abc123...",
    "character_frequency_map": { "r": 2, "a": 2, "c": 2, "e": 1 }
  },
  "created_at": "2025-10-21T14:00:00Z"
}
```

##🔹 2. Retrieve a Specific String

GET ``/strings/{string_value}``
Returns the analyzed properties of that string.

##🔹 3. Get All Strings (Filter Support)

GET ``/strings?is_palindrome=true&min_length=5&max_length=10&word_count=1&contains_character=a``
Returns matching strings and applied filters.

##🔹 4. Natural-Language Filtering

GET ``/strings/filter-by-natural-language?query=all%20single%20word%20palindromic%20strings``

Response
```JSON
{
  "data": [...],
  "count": 3,
  "interpreted_query": {
    "original": "all single word palindromic strings",
    "parsed_filters": {
      "word_count": 1,
      "is_palindrome": true
    }
  }
}
```
Supported query examples:

| Natural-Language Query                             | Interpreted Filters                        |
| -------------------------------------------------- | ------------------------------------------ |
| “all single word palindromic strings”              | `word_count=1, is_palindrome=true`         |
| “strings longer than 10 characters”                | `min_length=11`                            |
| “strings containing the letter z”                  | `contains_character=z`                     |
| “palindromic strings that contain the first vowel” | `is_palindrome=true, contains_character=a` |


##🔹 5. Delete String

DELETE ``/strings/{string_value} → 204 No Content``


###🧪 Testing with Postman

1. Create a new Postman collection.
2. Add each endpoint using the examples above.
3. Use JSON body for POST /strings.
4. Test filters and natural-language queries.
5. Check Swagger docs at /docs for schema reference.

```bash
# 1. Create
POST /strings
{ "value": "madam" }

# 2. List
GET /strings?is_palindrome=true

# 3. Natural language
GET /strings/filter-by-natural-language?query=all%20single%20word%20palindromic%20strings

# 4. Delete
DELETE /strings/madam
```

## 🧾 Dependencies

```ngnix
fastapi
uvicorn
```

# Install:
``` bash
pip install fastapi uvicorn
```

### 🌍 Deployment (recommended)

1. Push to GitHub.
2. Deploy on Railway.app, Heroku, PXXL App, or AWS EC2.
3. Set start command:

```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```
###🧠 Author

# Name: Olayide Olatunji
# Email: oloyeadz@gmail.com
# Stack: Python / FastAPI




