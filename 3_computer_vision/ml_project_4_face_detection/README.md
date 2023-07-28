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

At first, we'll use AWS Rekognition to perform celebrity facial recognition. This will allow us to set up the API calls and design patterns that will allow us to switch where we're getting our celebrity recognition predictions from with ease. Next, we'll move onto fine tuning our own celebrity recognition model and deploying it to VertexAI.

First, you need to create a service user on AWS:

* go to IAM
* create a User
* add policies directly
* give it the `AmazonRekognitionFullAccess` policy
* create the service user

Once you've created the service user in IAM, you need to generate a Access Key ID and Secret Key pair:

* select the user you just created, and click on the security credentials tab
* click create access key
* select one of the access key best practices & alternatives, then check the checkbox at the bottom saying "I understand the above recommendation and want to proceed to create an access key"
* click create access key
* download the CSV for the access key

This CSV file contains your access key id, and your secret key.

Go into your `~/.aws/credentials` file, and create a new entry like this:

```ini
[rekognition]
aws_access_key_id=<your access key id>
aws_secret_access_key=<your secret key>
```

Then, your backend should be able to access the rekognition celebrity detection API.
It looks for a profile called `rekognition` in your `~/.aws/credentials` file.

## Do Celebrity Facial Recognition with Resnet 50

Go into notebook 7, and follow the instructions in that notebook to fine tune the resnet 50 model on the celebrities dataset you've downloaded in the zip file.

You can find the instructions for importing models into VertexAI [here](https://cloud.google.com/vertex-ai/docs/model-registry/import-model).

You can find the instructions when you're using the pre-built TensorFlow containers [here](https://cloud.google.com/vertex-ai/docs/training/exporting-model-artifacts#tensorflow).

Basically, if you're using Keras, you run `model.save("path/to/savedModel/directory")`

At the end of that notebook, you should have a folder called `model` inside the `backend` directory. This `model` directory **is** the `SavedModel` artifact that you upload to TensorFlow.

Then you have to upload that `model` SavedModel directory into a Google Cloud Storage bucket, where Vertex AI can pick it up from.

### Upload model to Vertex AI

First, you need to create a cloud storage bucket location for your model:

1. go to Cloud Storage in the GCP console
2. create a bucket (with a unique name)
3. upload the `saved_model.pb` file from the `backend/model` directory

Now we need to import this model into the Vertex AI model registry:

1. go to Vertex AI in the GCP console
2. click on `Model Registry` in the left hand menu
3. click on `import`:
    * Import as new model
    * Name - set a name
    * Region - set the region to be same as your cloud storage bucket
    * Import model artifacts into a new pre-built container
    * Model framework - TensorFlow
    * Model framework version - 2.12
    * Accelerator type - None
    * Path to model artifact (this has to be the path to the directory containing your `saved_model.pb` file in your cloud storage bucket) - `gs://<bucket-name>`

Then you need to deploy this model that's in your model registry to a model endpoint:

* Click on the model in your model registry
* Click on Deploy & Test:
  * Endpoint name: celebrity-recognition


Finally, you need to add the IAM permission to the service account to make a call to the `aiplatform.endpoints.predict` API.

* go into IAM
* go to your service user, and click on the pencil all the way to the right of the table
* add another role:
  * add AI Platform Admin
