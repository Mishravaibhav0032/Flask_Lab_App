

import json
import datetime
import logging
from os import environ as env
from urllib.parse import quote_plus, urlencode
from flask import abort
from authlib.integrations.flask_client import OAuth
from dotenv import find_dotenv, load_dotenv
from flask import Flask, redirect, render_template, session, url_for



ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)


app = Flask(__name__)
app.secret_key = env.get("APP_SECRET_KEY")


oauth = OAuth(app)

oauth.register(
    "auth0",
    client_id=env.get("AUTH0_CLIENT_ID"),
    client_secret=env.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration'
)

@app.route("/login")
def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True)
    )
def requires_auth(f):
    def decorated(*args, **kwargs):
        if "user" not in session:
            app.logger.warning(f"UNAUTHORIZED ACCESS ATTEMPT: timestamp={datetime.datetime.utcnow()}")
            return abort(401)
        return f(*args, **kwargs)
    decorated.__name__ = f.__name__
    return decorated

@app.route("/callback", methods=["GET", "POST"])
def callback():
    token = oauth.auth0.authorize_access_token()
    session["user"] = token["userinfo"]  # Store user info only
    userinfo = session["user"]

    # Log the login event
    app.logger.info(f"LOGIN: user_id={userinfo['sub']}, email={userinfo['email']}, timestamp={datetime.datetime.utcnow()}")

    return redirect("/")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(
        "https://" + env.get("AUTH0_DOMAIN")
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("home", _external=True),
                "client_id": env.get("AUTH0_CLIENT_ID"),
            },
            quote_via=quote_plus,
        )
    )
@app.route("/protected")
@requires_auth
def protected():
    userinfo = session["user"]
    app.logger.info(f"PROTECTED ACCESS: user_id={userinfo['sub']}, timestamp={datetime.datetime.utcnow()}")
    return f"Welcome to the protected page, {userinfo['email']}!"

@app.route("/")
def home():
    return render_template("home.html", session=session.get('user'), pretty=json.dumps(session.get('user'), indent=4))

@app.errorhandler(401)
def unauthorized(e):
    # Optional: this logs again when Flask handles 401
    # You may keep it for visibility or remove if already logging in @requires_auth
    app.logger.warning(f"UNAUTHORIZED ACCESS HANDLED: timestamp={datetime.datetime.utcnow()}")
    return "Unauthorized", 401

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=env.get("PORT", 3000))
