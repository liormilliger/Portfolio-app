from flask import Flask, render_template, redirect, url_for, abort, request, has_request_context
from flask_bootstrap import Bootstrap
from flask_pymongo import PyMongo
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField
from datetime import date
from bson import ObjectId
import logging
import json
import os
from prometheus_client import Counter, generate_latest, Gauge
import time

app = Flask(__name__)

app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['MONGO_URI'] = os.environ.get('MONGO_URI')  # Set your MongoDB URI
mongo = PyMongo(app)
Bootstrap(app)
ckeditor = CKEditor(app)

class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "level": record.levelname,
            "message": record.getMessage(),
            "time": self.formatTime(record, self.datefmt)
        }
        if record.exc_info:
            log_record["exc_info"] = self.formatException(record.exc_info)
            return json.dumps(log_record)
        if has_request_context():
            log_record["method"] = request.method
        else:
            log_record["method"] = None
        return json.dumps(log_record)

# Initialize logger for the app
handler = logging.StreamHandler()
handler.setFormatter(JsonFormatter())
# Disable default Flask logging
log = logging.getLogger('werkzeug')
log.disabled = True
app.logger.handlers = []

app.logger.addHandler(handler)
app.logger.setLevel(logging.INFO)

class CreatePostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    author = StringField("Your Name", validators=[DataRequired()])
    img_url = StringField("Blog Image URL", validators=[DataRequired(), URL()])
    body = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = SubmitField("Submit Post")

total_requests = Counter('http_requests_total', 'Number of HTTP requests')
request_duration = Gauge('request_duration_seconds', 'Time spent processing a request', ['endpoint'])

@app.route('/')
def get_all_posts():
    start_time = time.time()
    total_requests.inc()
    app.logger.info('Fetching all posts')
    posts = mongo.db.blog.find()
    response = render_template("index.html", all_posts=posts)
    request_duration.labels(endpoint='/').set(time.time() - start_time)
    return response
    # return render_template("index.html", all_posts=posts)
    
def get_post(post_id):
    try:
        oid = ObjectId(post_id)
    except:
        abort(404)
    return oid

@app.route("/post/<post_id>")
def show_post(post_id):
    app.logger.info(f"new post {post_id}")
    requested_post = mongo.db.blog.find_one_or_404({"_id": get_post(post_id)})
    return render_template("post.html", post=requested_post)

@app.route("/new-post", methods=["GET", "POST"])
def add_new_post():
    app.logger.info('New-post')
    form = CreatePostForm()
    if form.validate_on_submit():
        new_post = {
            "title": form.title.data,
            "subtitle": form.subtitle.data,
            "body": form.body.data,
            "img_url": form.img_url.data,
            "author": form.author.data,
            "date": date.today().strftime("%B, %d, %Y")
        }
        mongo.db.blog.insert_one(new_post)
        return redirect(url_for("get_all_posts"))
    return render_template("make-post.html", form=form)

@app.route("/edit_post/<post_id>", methods=["GET", "PUT", "POST"])
def edit_post(post_id):
    app.logger.info('posts edit')
    post = mongo.db.blog.find_one_or_404({"_id": get_post(post_id)})
    edit_form = CreatePostForm(
        title=post["title"],
        subtitle=post["subtitle"],
        img_url=post["img_url"],
        author=post["author"],
        body=post["body"],
    )
    if edit_form.validate_on_submit():
        updated_post = {
            "title": edit_form.title.data,
            "subtitle": edit_form.subtitle.data,
            "img_url": edit_form.img_url.data,
            "author": edit_form.author.data,
            "body": edit_form.body.data,
        }
        mongo.db.blog.update_one({"_id": get_post(post_id)}, {"$set": updated_post})
        return redirect(url_for("show_post", post_id=get_post(post_id)))
    return render_template("make-post.html", form=edit_form, is_edit=True)

@app.route("/delete/<post_id>", methods=["GET", "DELETE"])
def delete_post(post_id):
    app.logger.info('Delete posts')
    mongo.db.blog.delete_one({"_id": get_post(post_id)})
    return redirect(url_for('get_all_posts'))

@app.route("/about")
def about():
    app.logger.info('About shit')
    return render_template("about.html")

@app.route("/contact")
def contact():
    app.logger.info('Dont ever call me again')
    return render_template("contact.html")

@app.route('/metrics')
def metrics():
    return generate_latest()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
