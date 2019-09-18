import flask
def recent_logs(recent_logs):
	return flask.render_template("recent.html", recent_logs=recent_logs)

