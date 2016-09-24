import os

auth0 = {
	"client_id": "XfzRDXArSkHFI9t21kdYMh9YnRA4be5Q",
	"domain": "rrees.eu.auth0.com",
	"client_secret": os.environ["AUTH0_SECRET"],
}

config = {
	"auth0": auth0,
}