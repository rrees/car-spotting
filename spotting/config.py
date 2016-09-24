import os

auth0 = {
	"client_id": "XfzRDXArSkHFI9t21kdYMh9YnRA4be5Q",
	"domain": "rrees.eu.auth0.com",
	"client_secret": os.environ["AUTH0_SECRET"],
}

callback_url = {
	'DEV': "http://localhost:5000",
	'PROD': "https://car-spotting.herokuapp.com",
}

config = {
	"auth0": auth0,
	"callback_url": callback_url,
}