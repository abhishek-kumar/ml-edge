# AiEdge Masterclass

This is the course repo for the content in the AiEdge AI Masterclass.

The structure of the repo consists of:

* 0_natural_language_processing (Weeks 4 & 5)
* 1_image_processing (Weeks 6 & 7)

Each directory contains the poetry configuration, Jupyter notebooks and application code to run all the examples given in the lectures, TA sessions, and the deployed applications for each section.


## Tech Stack

For this course, we'll be using the tools:

* `poetry`
* `TensorFlow`
* `GCP`

## Dev Setup

To install `poetry`, on Mac you can just go:

```bash
brew install poetry
```

If you're using Windows or Linux, you should follow the instructions [here](https://python-poetry.org/docs/).

First, you need to make sure you have some version of Python installed on your machine.

### Setup Poetry

For each of the sections, you have to `cd` into that directory, and install a poetry virtual environment with those specific dependencies.

You can instruct poetry to use the system version of Python with (if you're on Mac or Linux):

```bash
poetry env use $(which python)
```

If you're on Windows, you have to find the path to the currently active Python with:

```bash
gcm python
```

Then, copy that path into:

```bash
poetry env use <path-to-python>
```

Remember to remove the `<` and `>` when you paste in the path to your Python executable.

After running the `poetry env use` command, you should see something that looks like:

![Create poetry environment](img/image.png)

Then, to install all the dependencies from the `pyproject.toml`, you run:

```bash
poetry install
```
