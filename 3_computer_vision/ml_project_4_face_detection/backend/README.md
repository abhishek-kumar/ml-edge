# Backend

This is the backend service for the face detection project. It is a FastAPI application that exposes a REST API to upload images and detect faces in them.

The backend service calls GCP Face Detection and returns the bounding boxes to clients.

## Setup

To set up the backend, create your poetry virtual environment:

```bash
poetry env use $(which python)
```

Then install the dependencies:

```bash
poetry install --no-root
```

Then, you can run the backend FastAPI server with:

```bash
make app
```
