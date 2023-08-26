# FastAPI Backend

This is the code for creating the FastAPI backend for the sentiment analysis application.

To run this backend, you just need to:

1. Create a virtual environment:

```bash
python -m venv .backend-venv
```

2. Activate that virtual environment:

```bash
source .backend-venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Activate your gcloud default application credentials - this will make your backend utilize your user login so that we don't need to create a dedicated service user:

```bash
gcloud auth application-default login
```


5.  Start the FastAPI backend:

```bash
make backend
```

8. Test the backend out by navigating to `localhost:8080/api/review` in your browser.
