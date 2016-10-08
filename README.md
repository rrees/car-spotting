
# Car spotting

This is a simple web app to record interesting or unusual cars you see

## Development

You must set two environment variables:

* ENV (should be DEV)
* AUTH0_SECRET the client secret for the authentication system
* FIELDBOOK_CONFIG the JSON containing the API details for Fieldbook
* USER_EMAIL the email the service is for (the solution is not meant to be multi-tenanted)

## Third-party services

This application uses APIs from [Auth0](https://auth0.com/) and [Fieldbook](https://fieldbook.com/)