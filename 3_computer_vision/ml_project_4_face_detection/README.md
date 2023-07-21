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

## Run the Frontend

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

## Building

To create a production version of your app:

```bash
npm run build
```

You can preview the production build with `npm run preview`.