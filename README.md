# Tutorial #1: one branch to rule them all 🌳

> 🚨 Code in this repository is a supplementary material for the `One branch to
> rule them all` guided series on the [too long; automated
> blog](https://blog.toolongautomated.com). Here's a link to the first article
> in the series if you're interested:
[🔗 link](https://toolongautomated.com/posts/2024/one-branch-to-rule-them-all-1).

My goal in this tutorial is to show you how to:
- develop your code in a no-brainer git flow following permissive trunk-based branching strategy
- version your application using git tagging and Docker image tagging
- deploy the application to multiple environments (staging and production here, but you're free to do as many as you need)
- configure every deployment target separately using `.env` files
- **🚀 tl; a:** automate several steps by leveraging GitHub Actions

If you'd like to see how I've progressed through the implementation phase, I've
prepared several git tags marking important milestones. You either use `git
checkout [TAG_NAME]` to explore the code locally, or click on the link in the
list below to see it in GitHub's UI:

1. **Base version of the application** [[git tag
`1-reference-point`]](https://github.com/toolongautomated/tutorial-1/tree/1-reference-point):
    - simple flask server displaying welcome message
    - smoke unit test and integration tests placeholder
    - starter README
2. **Application versioning** [[git tag
`2-application-versioning`]](https://github.com/toolongautomated/tutorial-1/tree/2-application-versioning):
    - add changelog
    - containerize the app using Dockerfile
    - extend the readme to explain how to build and push Docker images to a dedicated Docker Hub registry
    - [diff](https://github.com/toolongautomated/tutorial-1/compare/1-reference-point...2-application-versioning) from the previous tag (to only see the changes)
3. **Environment configuration** [[git tag `3-environment-configuration`]](https://github.com/toolongautomated/tutorial-1/tree/3-environment-configuration):
    - add `deploy/environments` directory to store env-specific `.env` configuration files
    - [diff](https://github.com/toolongautomated/tutorial-1/compare/2-application-versioning...3-environment-configuration) from the previous tag (to only see the changes)
4. **Deployment** [[git tag `4-deployment`]](https://github.com/toolongautomated/tutorial-1/tree/4-deployment):
    - add `manage` bash script to streamline app deployment to Cloud Run
    - extend README to cover the deployment part of the development
    - [diff](https://github.com/toolongautomated/tutorial-1/compare/3-environment-configuration...4-deployment) from the previous tag (to only see the changes)

## Prerequisites

- `docker` >= 27.2.0
- `python` >= 3.10.4

## How to run locally

### Server

`app/src` directory contains a super simple Flask server that prints a welcome
message when a user enters `/` path.

First, install the requirements for the app (preferably in the virtual environment of your choice):

```shell
cd app
pip install -r requirements.txt
```

Then, run the server locally:

```shell
cd app/src
export FLASK_APP=main.py
gunicorn -w 4 -b 0.0.0.0:80 main:app
```

Then, go to `http://0.0.0.0:80`. You should see the welcome text:

![alt text](docs/welcome-screen.png)

### Tests

`app/test` directory is dedicated for unit and integration tests. I've prepared basic smoke test to start with.

To run the tests, first install the requirements (preferably in your virtual environment of choice):

```shell
cd app
pip install -r requirements-test.txt
```

Then, run the following:

```shell
pytest test/unit
```

## Introducing changes to the source code of the application

The application is versioned using [semantic versioning](https://semver.org/)
approach: whenever you add/remove/change any file strictly related to the
application, you should add new entry to the [CHANGELOG](app/CHANGELOG.md) file.
This can be: source code, requirements, static files that are used by the
application from within the container, this sort of things.

Below is a standard development you're expected to follow:

1. Create new feature branch from the `main` branch.
2. Introduce the changes to the application and put new entry in the
`CHANGELOG`, briefly describing the change.
3. Open PR to the `main` branch.
4. Once approved, merge the code.
5. Checkout the `main` branch locally and pull the changes.
6. Create a tag with the following command: `git tag [VERSION]`
7. Push the tag to the remote: `git push --tags`

## Docker image building and pushing

`app` directory contains a `Dockerfile` that encloses the app into a reusable
unit with requirements installed, networking set up, and all needed files copied
to ensure smooth execution.

I've also included a carefully crafted `.dockerignore` to ensure that only the
files that are truly required for the app's execution end up in the image.

### Build the image

Run the following to build the Docker image locally:

```shell
cd app
docker build -t tutorial-1 .
```

The image will be called `tutorial-1`. To run it, use the following command:

```shell
docker run --rm -p 80:80 tutorial-1
```

Note that it's NOT important from which directory you run it. Docker container
runs a Flask server inside, exposed to port 80 of the container. To make it
available outside of the container, we need to forward this port to some port
outside of the container. That's what the `-p` flag does–it forwards container's
port number 80 to port 80 of the local machine.

### Push the image

Once built, the image can be pushed to an external registry (a place on the
Internet where your Docker images are stored). For this tutorial, I've prepared
a repository on Docker Hub. You can access it
[here](https://hub.docker.com/r/toolongautomated/tutorial-1).

The repository is public, meaning anyone can freely pull the images from it, so
feel free to explore it if you are adventurous! Below, I'll be using this
repository to showcase sample Docker commands. However, please ensure you set up
your own registry and push the images to it instead of to the mine 🙌🏼

Okay, back to pushing.

First, authenticate to your image registry of choice. In my case it's the Docker
Hub, so I simply need to run:

```shell
docker login
```

Next, let's adjust the tags of the image we've already built before
(`tutorial-1`):

```shell
docker tag tutorial-1 toolongautomated/tutorial-1:1.0.0
```

Then, to push the built image:

```shell
docker push toolongautomated/tutorial-1:1.0.0
```

## Deployment to Cloud Run (example)

I think that giving you a chance to play with something real (cloud) instead of
a local playground (your machine) will be invaluable. I’ve analyzed [free
tier](https://cloud.google.com/free/docs/free-cloud-features) rules of the
Google Cloud Platform and realized that **Cloud Run** will be a perfect choice
to play with multi-environment deployment tutorial. It is because for our short
experiments, **it’ll be free to use**.

**tl;dr:** Cloud Run lets you run your app in containers without worrying about
servers. It scales up and down as needed and only costs when it’s running. It’s
great for small services and APIs.

If you’d like this tutorial to be a true hands-on experience, I highly encourage
you to set up a GCP project and play with it in the rest of this tutorial. I’ve
prepared a short video on how to create a new project if this is your first time
doing it: [link](https://youtu.be/pC2dBysvhwI).

### `gcloud` setup

Google provides a dedicated CLI tool to manipulate GCP infrastructure from a
local machine. It’s called `gcloud` and
[here](https://cloud.google.com/sdk/docs/install) are the instructions on how to
install it.

Once installed, you need to authorize gcloud:

```shell
gcloud auth login
gcloud auth application-default login
```

Then, we need to set the GCP project that all gcloud commands will run against:

```shell
gcloud config set project [YOUR-PROJECT-ID]
```

Finally, the quota project needs to also be set to this project ID:

```shell
gcloud auth application-default set-quota-project [YOUR-PROJECT-ID]
```

### Deploy

`deploy/environments` directory contains subdirectories, each storing a `.env`
file associated with the deployment environment. Name of the subdirectory
corresponds to the name of the environment it serves (case-specific!).

To deploy the application:
1. Build the Docker image and push it to the registry of your choice (GCP's
    Artifact Registry and Docker Hub are natively supported by Cloud Run).
2. Prepare the `.env` file for your deployment.
3. Run the following command:
    ```shell
    ./manage deploy [ENVIRONMENT]
    ```
    where `[ENVIRONMENT]` should be substituted with the actual name of your
    environment, e.g. `staging`.
4. Once done playing with the deployment, remove it to avoid unnecessary cloud costs. To terminate Cloud Run deployment, run:
    ```shell
    gcloud run services delete [SERVICE_NAME] \
        --region [REGION]
    ```
