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
```
git clone https://github.com/<your-username>/string-analyzer-service.git
cd string-analyzer-service/app
```

### 2️⃣ Create Virtual Environment
```
python -m venv venv
venv\Scripts\activate      # Windows
# source venv/bin/activate  # macOS/Linux
```

### 3️⃣ Install Dependencies
```
pip install -r requirements.txt
```
### 4️⃣ Run Locally
From the project root:

```
uvicorn app.main:app --reload
```
Server will start at:
👉 http://127.0.0.1:8000

Swagger Docs: http://127.0.0.1:8000/docs

### 🧠 API Endpoints

## 🔹 1. Create & Analyze String
POST /strings

```
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








