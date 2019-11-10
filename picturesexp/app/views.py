from app.tasks import create_image_set
from flask import render_template, request, flash
from app import app, q
from pathlib import Path

import os
import secrets

app.config["SECRET_KEY"] = "liruhfoi34uhfo8734yot8234h"
upload_directory = "/Users/petrosxen/resources/redisexperimenting/picturesexp/app/static/img/uploads"

rel_path = "/static/img/uploads"
# base_path = Path(__file__).parent

# upload_directory = (base_path / "static/img/uploads")

print(upload_directory)
# upload_directory="/static/img/uploads"

@app.route("/upload-image", methods=["GET", "POST"])
def upload_image():

    message = None

    if request.method == "POST":

        image = request.files["image"]

        image_dir_name = secrets.token_hex(16)

        os.mkdir(os.path.join(upload_directory, image_dir_name))

        image.save(os.path.join(upload_directory, image_dir_name, image.filename))

        image_dir = os.path.join(upload_directory, image_dir_name)

        print(image.filename)
        print(image_dir)

        q.enqueue(create_image_set, image_dir, image.filename)

        flash("Image uploaded and sent for resizing", "success")

        message = f"/image/{image_dir_name}/{image.filename.split('.')[0]}"

    return render_template("upload_image.html", message=message)    

# web_friendly = upload_directory.replace(" ")

# print(web_friendly)

@app.route("/image/<dir>/<img>")
def view_image(dir, img):
    return render_template("view_image.html", dir=dir, img=img, src=rel_path,extension="jpg")
