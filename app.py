import os
from os.path import join, dirname
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGODB_URI = os.environ.get("MONGODB_URI")
DB_NAME = os.environ.get("DB_NAME")

client = MongoClient(MONGODB_URI)
db = client[DB_NAME]

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/fanbook", methods=["POST"])
def fanbook_post():
    fanbook_receive = request.form['fanbook_give']
    doc = {
        'fabook': fanbook_receive,
        'done': 0  # Set to 0 as it's not done yet
    }
    db.fanbook.insert_one(doc)
    return jsonify({'msg': 'Fan book message saved!'})

@app.route("/fanbook", methods=["GET"])
def fanbook_get():
    fanbook_list = list(db.fanbook.find({}, {'_id': False}))
    return jsonify({'fanbooks': fanbook_list})

@app.route("/fanbook/done", methods=["POST"])
def fanbook_done():
    num_receive = int(request.form['num_give'])
    db.fanbook.update_one({'num': num_receive}, {'$set': {'done': 1}})
    return jsonify({'msg': 'Fan book message marked as done!'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)

