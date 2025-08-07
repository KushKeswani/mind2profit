# Mind2Profit Backend

## Setup

1. Create and activate a virtual environment:
   ```bash
   python3 -m venv backend-venv
   source backend-venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the server

```bash
uvicorn main:app --reload
```

The API will be available at http://127.0.0.1:8000 