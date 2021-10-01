from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient

from datetime import datetime

app = Flask(__name__)

client = MongoClient("mongodb://localhost:27017/")
db = client.dbStock


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/post', methods=['POST'])
def save_post():
    receive_title = request.form["title_give"]
    receive_content = request.form["content_give"]

    today = datetime.now()
    mytime = today.strftime('%Y.%m.%d %H:%M:%S')

    one = db.posts.find_one({'idx': 1}, {'_id': False})
    idx = one['idx'] + 1



    doc = {
        'idx' : idx,
        'title': receive_title,
        'content': receive_content,
        'reg_date': mytime
    }

    db.posts.insert_one(doc)
    return jsonify({"result": "success", "msg": "포스팅 성공"})


@app.route('/post', methods=['GET'])
def get_post():
    post_list = list(db.posts.find({}, {"_id": False}))
    return jsonify({"result": "success", "post_list": post_list})


@app.route('/post', methods=['DELETE'])
def delete_post():
    db.posts.delete_one({})
    return jsonify({"result": "success"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
