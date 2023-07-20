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

## GCP Setup

* go to IAM
* create a service user
  * call it `cloud-vision-service-user`
  * give it the `VisionAI Admin` role
* then click on the Sandwhich to the right of the service user on the service user page
* click on Manage Keys
* Click Add Key -> Create new key -> JSON
 
Then, you need to enable your cloud vision API:
* type in Cloud Vision API in the search bar
* click on the Cloud Vision API
* click Enable


Whenever you make commands that depend on the Cloud Vision API, you have to set the environment variable `GOOGLE_APPLICATION_CREDENTIALS` to the path of the JSON file you downloaded.
