from flask import Flask, render_template, redirect, url_for, abort, request
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

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['MONGO_URI'] = os.environ.get('MONGO_URI')  # Set your MongoDB URI
mongo = PyMongo(app)
Bootstrap(app)
ckeditor = CKEditor(app)

class CreatePostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    author = StringField("Your Name", validators=[DataRequired()])
    img_url = StringField("Blog Image URL", validators=[DataRequired(), URL()])
    body = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = SubmitField("Submit Post")

class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "time": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "message": record.getMessage()
        }
        if record.exc_info:
            log_record["exc_info"] = self.formatException(record.exc_info)
        return json.dumps(log_record)

# Initialize the Flask app
app = Flask(__name__)
# ... other app configurations ...

# Setup logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)
log_handler = logging.FileHandler('app.log')
log_handler.setFormatter(JsonFormatter())
logger.addHandler(log_handler)

def log_request_info():
    logger.info(f"Request: {request.method} {request.url} from {request.remote_addr}")


@app.route('/')
def get_all_posts():
    try:
        posts = mongo.db.blog.find()
        logger.info("Processed request successfully.")
        return render_template("index.html", all_posts=posts)
    except Exception as e:
        logger.error(f"Error processing request: {e}", exc_info=True)
    
def get_post(post_id):
    try:
        oid = ObjectId(post_id)
    except:
        abort(404)
    return oid

@app.route("/post/<post_id>")
def show_post(post_id):
    requested_post = mongo.db.blog.find_one_or_404({"_id": get_post(post_id)})
    return render_template("post.html", post=requested_post)

@app.route("/new-post", methods=["GET", "POST"])
def add_new_post():
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
    mongo.db.blog.delete_one({"_id": get_post(post_id)})
    return redirect(url_for('get_all_posts'))

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
