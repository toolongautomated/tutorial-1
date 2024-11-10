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
