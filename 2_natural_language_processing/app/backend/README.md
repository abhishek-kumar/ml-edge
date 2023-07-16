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

4. Then, you need to go into your GCP console, and create a service user that can perform all Bigquery and VertexAI commands.

5. Once you have that service user, you need to create a key for that user (download a JSON file containing a private key to assume that user).

6. Place that key in the `backend` directory

7. Edit value of the `GOOGLE_APPLICATION_CREDENTIALS` environment variable in the `Makefile` with the path to this key file.

8. Start the FastAPI backend:

```bash
make backend
```

9. Test the backend out by navigating to `localhost:8080/api/review` in your browser.
