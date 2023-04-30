import os
import json
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from flask import send_from_directory
import random as r
from libs.chatgpt import gpt
from libs.imagetotext import imagetotext
from libs.speechtotext import transcribe_audio
import glob
import datetime
import db as db
import requests
import hashlib
import boto3
from flask import Response
from flask import jsonify
import json
import libs.get_similarities as gs
from flask_cors import CORS, cross_origin
import random
import weasyprint
from weasyprint import HTML

app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'
UPLOAD_FOLDER = 'documents'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
r2_key_id = "5c2fbe75ef72800a657b2162e26f9d9e"
r2_secret = "dc4e30e63e3b92c8dcd6f3ab1682dbb0006447cb976312fd0f2593b566350d76"
r2_url = "https://a5bf26d175b4ef522050eb96f8d8e4a0.r2.cloudflarestorage.com/tumai"

s3 = boto3.resource('s3',
                    endpoint_url=r2_url,
                    aws_access_key_id=r2_key_id,
                    aws_secret_access_key=r2_secret)
bucket = s3.Bucket('tumai')


@app.route("/*", methods=["OPTIONS"])
@cross_origin()
def hello_world_options():
    return "Work I did"


@app.route("/")
@cross_origin()
def hello_world():
    return "Work I did"


@app.route("/projects", methods=["POST"])
@cross_origin()
def create_project():
    new_project = request.get_json()
    print(new_project)
    id = db.create_Project(
        new_project["name"], new_project["address"], new_project["date"])
    return Response(status=201)


@app.route("/projects", methods=["GET"])
@cross_origin()
def get_projects():
    res = db.get_all_Projects()
    arr = []
    for i in res:
        arr.append(i.to_dict())
    return jsonify(arr)


@app.route("/projects/<project_id>/tasks")
@cross_origin()
def get_tasks_for_project(project_id):
    res = db.get_Tasks_for_Project(project_id)
    arr = []
    for i in res:
        arr.append(i.to_dict())
    return jsonify(arr)


@app.route("/tasks", methods=["POST"])
@cross_origin()
def create_task():
    new_task = request.get_json()
    id = db.create_Task(new_task["name"], new_task["project_id"])
    return Response(status=201)


@app.route("/tasks/<task_id>/file/<language>", methods=["POST"])
@cross_origin()
def create_file(task_id, language):
    print(request.files)
    file = request.files['file']
    name = file.filename
    bucket.upload_fileobj(file, name)
    db.create_File(name, task_id, language)
    return Response(status=201)


@app.route("/tasks/<task_id>/file/<language>", methods=["GET"])
@cross_origin()
def get_files(task_id, language):
    files = db.get_all_Files(task_id)

    original = ""
    translated = ""
    for file in files:
        print("FILENAME: " + file.name)
        bucket.download_file(file.name, f"{UPLOAD_FOLDER}/{file.name}")
        extension = file.name.rsplit('.', 1)[1].lower()
        if extension == "jpg":
            text = imagetotext(f"{UPLOAD_FOLDER}/{file.name}")
            original += "\n" + text
            if file.language is not language:
                translated += gs.translate_text(language, text)
            else:
                translated += "\n" + text
        elif extension == "mp3":
            text = transcribe_audio(f"{UPLOAD_FOLDER}/{file.name}")
            original += "\n" + text
            if file.language is not language:
                translated += gs.translate_text(language, text)
            else:
                translated += "\n" + text
        elif extension == "txt":
            f = open(f"{UPLOAD_FOLDER}/{file.name}", "r")
            text = f.read()
            original += "\n" + text
            if file.language is not language:
                translated += gs.translate_text(language, text)
            else:
                translated += "\n" + text
    if translated is original:
        return jsonify({"original_text": original, "similarity_score": -1, "original_language": files[0].language, "translated_text": translated})
    else:
        return jsonify({"original_text": original, "similarity_score": gs.get_similarity_scores(original, translated, files[0].language), "original_language": files[0].language, "translated_text": translated})


def get_files_2(task_id, language):
    files = db.get_all_Files(task_id)
    original = ""
    translated = ""
    for file in files:
        bucket.download_file(file.name, f"{UPLOAD_FOLDER}/{file.name}")
        extension = file.name.rsplit('.', 1)[1].lower()
        if extension == "jpg":
            text = imagetotext(f"{UPLOAD_FOLDER}/{file.name}")
            original +=  "\n"+ text
            if file.language is not language:
                translated += gs.translate_text(language, text)
            else:
                translated += "\n" + text
        elif extension == "mp3":
            text = transcribe_audio(f"{UPLOAD_FOLDER}/{file.name}")
            original +=  "\n" + text
            if file.language is not language:
                translated += gs.translate_text(language, text)
            else:
                translated += "\n" + text
        elif extension == "txt":
            f = open(f"{UPLOAD_FOLDER}/{file.name}", "r")
            text = f.read()
            original +=  "\n" + text
            if file.language is not language:
                translated += gs.translate_text(language, text)
            else:
                translated += "\n" + text
    return translated

@app.route("/file/<file_id>", methods=["GET"])
@cross_origin()
def file(file_id):
    file = db.get_File(file_id)
    bucket.download_file(file.name, f"{UPLOAD_FOLDER}/{file.name}")
    return send_from_directory(app.config["UPLOAD_FOLDER"], f"{file.name}")


@app.route("/tasks/<task_id>", methods=["PUT"])
@cross_origin()
def update_task(task_id):
    body = request.get_json()
    textfile = body["text"]
    print(textfile)
    identifier = random.randint(0, 100000)
    save_name = f"text{task_id}_{identifier}.txt"
    f = open(save_name, "w")
    f.write(textfile)
    f.close()
    textfile = open(save_name, "rb")
    bucket.upload_file(save_name, save_name)
    db.create_File(save_name, task_id, body["language"])

    new_task = request.get_json()
    db.update_Task(task_id)
    return Response(status=201)

@app.route("/projects/pdf/<project_id>", methods=["GET"])
@cross_origin()
def get_pdf(project_id):
    html = '''<div style="font-family: 'Courier New', Courier, monospace; font-size: xx-small;">
    <hr />
    <h1>
<p style="text-align: center;"><strong>Project report'''
    html += f" ({datetime.datetime.now():%d.%m.%Y})"
    html += '''</strong></p>
</h1><hr />
<p style="text-align: left;">'''
    tasks = db.get_Tasks_for_Project(project_id)
    i = 1
    for task in tasks:
        html += f"<h2>Task {i}: {task.name}</h2>"
        i += 1
        html += get_files_2(task.id, "en") 
        html += "<br /><br />"
    html + "</p></div>"
    pdf = HTML(string=html).write_pdf()
    with open(f'{UPLOAD_FOLDER}/output.pdf', 'wb') as f:
        f.write(pdf)

    return send_from_directory(app.config["UPLOAD_FOLDER"], "output.pdf")

app.run(host="0.0.0.0")
