import os
from flask import Flask, render_template, request, jsonify
from os.path import join, dirname
from dotenv import load_dotenv
from http import client
from pymongo import MongoClient
from datetime import datetime

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGODB_URI = os.environ.get("MONGODB_URI")
DB_NAME =  os.environ.get("DB_NAME")

client = MongoClient(MONGODB_URI)

db = client[DB_NAME]

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/diary', methods=['GET'])
def show_diary():
    # sample_receive = request.args.get('sample_give')
    # print(sample_receive)
    articles = list(db.diary.find({}, {'_id' : False}))
    return jsonify({'articles' : articles})

@app.route('/diary', methods=['POST'])
def save_diary():
    # sample_receive = request.form['sample_give']
    # print(sample_receive)
    title_receive = request.form['title_give']
    content_receive = request.form['content_give']

    today = datetime.now()
    mytime = today.strftime('%Y-%m-%d-%H-%M-%S')

    file = request.files["file_give"]
    extension = file.filename.split('.')[-1]
    filename = f'static/img/post-{mytime}.{extension}'
    file.save(filename)


    
    profile = request.files["profile_give"]
    extension = profile.filename.split('.')[-1]
    profilename = f'static/img/profile-{mytime}.{extension}'
    profile.save(profilename)

    doc = {
        'profile' : profilename,
        'time' : mytime,
        'file' : filename,
        'title' : title_receive,
        'content' : content_receive
    }

    db.diary.insert_one(doc)
    return jsonify({'msg' : 'POST request success'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=500, debug=True)