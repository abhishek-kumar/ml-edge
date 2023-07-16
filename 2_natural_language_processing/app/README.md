# Full Stack Sentiment Analysis Application

This app is a very basic implementation of an application that can take in reviews from the user, send those reviews to an LLM hosted on GCP VertexAI,
and then make a prediction as to whether the sentiment of that review is positive or negative.

There are two main components to this app:

* the Python-based FastAPI backend service
* the Svelte (JavaScript)-based frontend client (service)

The frontend for the app looks like this:

![Alt text](frontend.png)
