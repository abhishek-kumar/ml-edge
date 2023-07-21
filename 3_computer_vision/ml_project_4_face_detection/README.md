# Face Detection Project

In this project, we'll build a full stack face detection application.

The technical components will consist of:

* Svelte.js frontend
* Python/FastAPI backend
* GCP VertexAI Face detection

## Frontend

This `frontend` folder was generated with the command:

```bash
npm create svelte@latest frontend
```

Then, I selected:

* `Skeleton project`
* `Yes, using TypeScript syntax`
* Leave all options blank and hit enter

### Run the Frontend

First, install the dependencies:

```bash
npm install

# or
make install
```

Then run the frontend server:

```bash
npm run dev

# or start the server and open the app in a new browser tab
npm run dev -- --open

# or 
make run
```

### Building

To create a production version of your app:

```bash
npm run build
```

You can preview the production build with `npm run preview`.

## Backend

This is the backend service for the face detection project. It is a FastAPI application that exposes a REST API to upload images and detect faces in them.

The backend service calls GCP Face Detection and returns the bounding boxes to clients.

### Setup

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

### GCP Setup

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

Whenever you make commands that depend on the Cloud Vision API, you have to set the environment variable `GOOGLE_APPLICATION_CREDENTIALS` to the path of the JSON file you downloaded.p

### Face Recongition

First, download the celebrity images dataset from [this Google Drive link](https://drive.google.com/file/d/15SK4cTePa20TYOZmx8qNqXI-v4GIozIq/view?usp=drive_link).

Move that zip file into the `backend` directory.

Then, unzip that archive:

```bash
unzip celebrity-18.zip
```

This will create a folder called `Celebrity Faces Dataset` on your machine.
