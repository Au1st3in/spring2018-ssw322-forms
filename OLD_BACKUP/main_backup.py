import os, json

from flask import Flask, jsonify
from flask_oauth2_login import GoogleLogin

with open('config.json') as cfg:
    config = json.load(cfg)

app = Flask(__name__)
app.config.update(
    SECRET_KEY= config["google_oauth"]["client_secret"],
    GOOGLE_LOGIN_REDIRECT_SCHEME="http",
    GOOGLE_LOGIN_CLIENT_ID=config["google_oauth"]["client_id"],
    GOOGLE_LOGIN_CLIENT_SECRET=config["google_oauth"]["client_secret"]
)

google_login = GoogleLogin(app)

@app.route("/")
def index():
    return """
<html>
<a href="{}">Login with Google</a>
""".format(google_login.authorization_url())

@google_login.login_success
def login_success(token, profile):
    return jsonify(token=token, profile=profile)

@google_login.login_failure
def login_failure(e):
    return jsonify(error=str(e))

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
