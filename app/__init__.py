import os
from flask import Flask, render_template, redirect, url_for, request
from dotenv import load_dotenv
import hashlib

from peewee import (
    MySQLDatabase,
    Model,
    CharField,
    TextField,
    DateTimeField,
)
from playhouse.shortcuts import model_to_dict
import datetime


def md5_hash_email(email):
    md5_hasher = hashlib.md5()
    md5_hasher.update(email.encode("utf-8"))
    hashed_email = md5_hasher.hexdigest()
    return hashed_email


load_dotenv()
app = Flask(__name__, template_folder="../templates", static_folder="../static")
app.jinja_env.globals.update(md5_hash_email=md5_hash_email)

mydb = MySQLDatabase(
    os.getenv("MYSQL_DATABASE"),
    user=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD"),
    host=os.getenv("MYSQL_HOST"),
    port=3306,
)


class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = mydb


mydb.connect()
mydb.create_tables([TimelinePost])
URL = os.getenv("URL")


def check_errors(form: dict):
    errors = []
    if "name" not in form:
        errors.append("Invalid name")
    if "email" not in form:
        errors.append("Invalid email")
    if "content" not in form:
        errors.append("Invalid content")
    return errors


@app.route("/timeline", methods=["POST"])
def post_time_line_post():
    errors = check_errors(request.form)
    if errors:
        return {"errors": errors}, 400

    name = request.form["name"].strip()
    email = request.form["email"].strip()
    content = request.form["content"].strip()

    TimelinePost.create(name=name, email=email, content=content)
    return redirect(url_for("timeline"))


@app.route("/api/timeline_post", methods=["POST"])
def api_post_time_line_post():
    errors = check_errors(request.form)
    if errors:
        return {"errors": errors}, 400

    name = request.form["name"].strip()
    email = request.form["email"].strip()
    content = request.form["content"].strip()

    timeline_post = TimelinePost.create(name=name, email=email, content=content)
    return model_to_dict(timeline_post), 200


@app.route("/api/timeline_post", methods=["DELETE"])
def delete_time_line_post():
    errors = check_errors(request.form)
    if errors:
        return {"errors": errors}, 400

    name = request.form["name"]
    email = request.form["email"]
    content = request.form["content"]
    timeline_post = TimelinePost.get_or_none(name=name, email=email, content=content)

    if timeline_post is None:
        return {"error": "Timeline post does not exist"}, 400
    timeline_post.delete_instance()

    return model_to_dict(timeline_post), 200


@app.route("/api/timeline_post", methods=["GET"])
def get_timeline_post():
    return {
        "timeline_posts": [
            model_to_dict(p)
            for p in TimelinePost.select().order_by(TimelinePost.created_at.desc())
        ]
    }, 200


@app.route("/")
@app.route("/index")
def index():
    """Our default routes of '/' and '/index'

    Return: The content we want to display to a user
    """

    return render_template("index.html", title="Home", url=URL), 200


@app.route("/education")
def education():
    return render_template("education.html", title="Education", url=URL), 200


@app.route("/timeline", methods=["GET"])
def timeline():
    posts = [p for p in TimelinePost.select().order_by(TimelinePost.created_at.desc())]

    return (
        render_template(
            "timeline.html",
            title="Timeline",
            posts=posts,
            url=URL,
        ),
        200,
    )


@app.route("/timeline/search", methods=["GET"])
def search_timeline():
    # search for posts containing the search term
    query: str | None = request.args.get("query")

    if query is None:
        return redirect(url_for("timeline"))

    posts = [
        p
        for p in TimelinePost.select().order_by(TimelinePost.created_at.desc())
        if query.lower() in p.content.lower()
    ]

    return (
        render_template(
            "timeline.html",
            title="Timeline",
            posts=posts,
            url=URL,
        ),
        200,
    )


@app.route("/map")
def map():
    return render_template("map.html", title="Map", url=URL), 200


@app.route("/work")
def work():
    return render_template("work.html", title="Work", url=URL), 200


@app.route("/hobbies")
def hobbies():
    return render_template("hobbies.html", title="Hobbies", url=URL), 200


@app.route("/<path:path>")
def catch_all(path):
    """A special route that catches all other requests

    Note: Let this be your last route. Priority is defined
    by order, so placing this above other functions will
    cause catch_all() to override then.

    Return: A redirect to our index route
    """

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
