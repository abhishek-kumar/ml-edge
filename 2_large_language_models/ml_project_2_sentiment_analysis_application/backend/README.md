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

4. Go into the GCP console, and then to IAM. On the left hand tab, you should see a panel for Service Accounts. Create a service account here. Make sure to add the VertexAI user role and the Bigquery user role when creating the service user.

5. Then, click on the three dots to the right of that service account, and click on `Manage Keys`. Then, hit `Add Key` and `Create new key`. Make sure you make one of JSON type. Download that key and put it in the `backend` directory.
6. Go into the `Makefile`, and replace `aiedge-bigquery-llm-inference-e5a944517046.json` with the name of your file.

7.  Start the FastAPI backend:

```bash
make backend
```

8. Test the backend out by navigating to `localhost:8080/api/review` in your browser.
