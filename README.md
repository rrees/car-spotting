
# Car spotting

This is a simple web app to record interesting or unusual cars you see

## Development

You must set two environment variables:

* ENV (should be DEV)
* USER_EMAIL the email the service is for (the solution is not meant to be multi-tenanted)
* PASSWORD fixed password to login with

## Deployment

This app uses a custom Dockerfile rather than a Buildpack based one so remember to upgrade the Python version update both the base image and the Pipfile version