# MatchMaker

> Connecting researchers with the funding they actually deserve.

Most researchers receive funding that doesn't align with their work. MatchMaker exists to fix that — describe your research project, upload supporting documents, and MatchMaker returns a ranked list of grant opportunities that are actually right for you.

---

## Features

- Grant search across grants.gov and Northwestern University Foundation Relations
- Results ranked by relevance to your project
- Keyword refinement to tune results after your first search
- Filter by status, funding source, and award amount
- Save grants to a personal list
- User profile page

---

## Tech Stack

- Python 3 / Flask
- DeepSeek API for keyword extraction and ranking
- HTML / CSS / Vanilla JavaScript

---

## Setup

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd MatchMaker
```

### 2. Create and activate a virtual environment
```bash
# macOS / Linux
python -m venv venv
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Add your API key

Create a file called `api_key.py` in the root directory:
```python
api_key = "your-deepseek-api-key-here"
```

> `api_key.py` is in `.gitignore` — never commit it. Each team member needs their own local copy.

### 5. Run the app
```bash
python app.py
```

Open `http://127.0.0.1:5000` in your browser. Enter any email and password to log in.

---

## Routes

| Route | Description |
|---|---|
| `/login` | Login page |
| `/` | Main search form |
| `/search` | Processes submission and runs grant search |
| `/results` | Displays ranked results |
| `/edit-search` | Re-runs search with edited keywords |
| `/saved` | Saved grants |
| `/profile` | User profile |

---

## Notes

- Login is a placeholder — any credentials will work
- Saved grants are stored in browser localStorage, not a database
- Filters are UI-only and not yet wired into the backend search

---

## Team

Ananya, Hongbo, Nicholas
