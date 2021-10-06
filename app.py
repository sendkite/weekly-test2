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
    title = request.form.get('title')
    content = request.form.get('content')

    # 다큐먼트 개수를 반환
    post_count = db.posts.count()
    if post_count == 0:
        max_value = 1
    else:
        max_value = db.posts.find_one(sort=[("idx", -1)])["idx"] + 1
    print(max_value)

    post = {
        'idx': max_value,
        'title': title,
        'content': content,
        'reg_date': datetime.now()
    }
    db.posts.insert_one(post)

    return jsonify({"result": "success"})


@app.route('/post', methods=['GET'])
def get_post():
    posts = list(db.posts.find({}, {'_id': False}))
    return {"result": "success", "posts": posts}


@app.route('/post', methods=['DELETE'])
def delete_post():
    idx = request.form.get("idx")

    db.posts.delete_one({"idx": int(idx)})
    return {"result": "success"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
