# GitHub Actions workflows

Below are the details on the GitHub Actions workflows used in this project that
automate:

- git tags
- build and push Docker images to Docker Hub
- deploy application to Cloud Run
- unit and integration tests

## git tags

Whenever a new version of the application is released, a new git tag is created.

It is done automatically through the `tag_build_push` GitHub Actions workflow.
This workflow triggers on pushes to the `main` branch, whenever changes are made
to application-related files.

The workflow relies on the `app/CHANGELOG.md` and requires it to follow a
specific format:

```md
# Sample changelog file

## 1.0.1

Changes description...

## 1.0.0

Initial release...
```

- each version must be a level-2 header (`##`)
- version numbers must follow semantic versioning (`X.Y.Z`)
- latest version should be at the top of the file

The workflow will fail if:

❌ application-related files are modified without updating changelog

❌ changelog version unchanged from previous version

❌ new tag would be created but it already exists

## Build and push Docker images to Docker Hub

Once the tag is successfully created, the `tag_build_push` workflow proceeds to
building a Docker image and pushing it to Docker Hub (registry provider used
purely for illustrative purposes).

To push images to Docker Hub, a personal access token (PAT) with the necessary
permissions is required. You can create a PAT using a dedicated [Docker Hub
settings page](https://app.docker.com/settings/personal-access-tokens).

Ensure that the token has `Read & Write` scopes.

Once the PAT is created, it needs to be added to the GitHub repository secrets:

1. Go to the repository settings, click on `Secrets and variables`, and then
   click on `New repository secret`.
1. Add two secrets: `DOCKER_USERNAME` (Docker Hub account username) and
   `DOCKER_TOKEN` (PAT).

## Deploy application to Cloud Run

`deploy/environments` directory contains subdirectories, each storing a `.env`
file associated with the deployment environment. Name of the subdirectory
corresponds to the name of the environment it serves (case-specific!).

---

Google Cloud Platform offers a [free
tier](https://cloud.google.com/free/docs/free-cloud-features). As part of it (as
of 2025-01-20), you can use Cloud Run for free (to some extent). Cloud Run lets
you run your app in containers without worrying about servers. It scales up and
down as needed and only costs when it's running. It's great for small services
and APIs.

The `deploy` GitHub Actions workflow can deploy the application to Cloud Run.
It will be triggered on every push to the `main` branch, whenever any of the
`.env` files gets modified.

If multiple `.env` files are modified, the workflow will deploy the application
to all affected environments.

If you'd like to try it out, you need to set up a GCP project first. Here's [a
short video](https://youtu.be/pC2dBysvhwI) on how to create a new project if
this is your first time doing it.

> In this tutorial, **Workload Identity Federation** is used to authenticate
> GitHub Actions workflow to GCP (as a safer alternative to service accounts).
> Explaining this mechanism is beyond the scope of this tutorial, but you can read
> more about it
> [here](https://cloud.google.com/iam/docs/workload-identity-federation).

To use Workload Identity Federation, several resources need to be created.
Install `gcloud` CLI and use `setup-iam` command from the `manage` script to
configure:

- a new workload identity pool for GitHub Actions
- a new provider for the GitHub Actions pool
- a new IAM role for the GitHub Actions pool
- a new IAM policy binding for the GitHub Actions pool


The command template is:
```shell
./manage setup-iam [REPO_OWNER] [REPO_NAME] [PROJECT_ID]
```

Example:

```shell
./manage setup-iam toolongautomated tutorial-1 toolongautomated
```

`setup-iam` outputs the full identity provider name. Use it in the `deploy`
GitHub Actions workflow:

```yaml
- name: 'Authenticate to Google Cloud'
  uses: 'google-github-actions/auth@v2'
  with:
    project_id: '[GCP_PROJECT_ID]'
    workload_identity_provider: '[FULL_PROVIDER_NAME]'
```

Example:

```yaml
- name: 'Authenticate to Google Cloud'
  uses: 'google-github-actions/auth@v2'
  with:
    project_id: 'toolongautomated'
    workload_identity_provider: 'projects/572404090605/locations/global/workloadIdentityPools/github/providers/tutorial-1'
```

🚨 **Remember**

Once done playing with the Cloud Run deployment, remember to delete the service.
Otherwise, you may be charged for running it for too long outside of the free
tier. Read more about it [here](https://www.toolongautomated.com/posts/2025/one-branch-to-rule-them-all-3.html#deploy-to-cloud-run).

`delete` command can be used to delete the service:

```shell
./manage delete [ENVIRONMENT] [PREFIX]
```

Prefix is optional and will be attached to the service name. Example:

```shell
./manage delete staging test
```

This will attempt to delete the service `test-[SERVICE NAME]-staging`.

## Unit tests

Whenever a pull request is opened or a new commit is added to it, the
`test_unit` workflow will be executed. It will run unit tests and publish the
results to the PR as a comment if any of the application-related files are
modified.

## Integration tests

The `test_integration` workflow runs integration tests whenever `.env` files are modified in a pull request. For each modified environment:

1. Deploys a test instance to Cloud Run with `test-` prefix.
2. Runs integration tests against the deployed instance.
3. Posts test results as a PR comment.
4. Deletes the test instance.

The workflow requires the same GCP authentication setup as the `deploy` workflow.
