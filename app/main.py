import time
import random
from flask import Flask, jsonify, request

app = Flask(__name__)

posts = [
    {"id": 1, "author": "Admin", "title": "First Post", "content": "Hype Rocks!"},
    {"id": 2, "author": "User1", "title": "Another One", "content": "Totally agree"},
]
next_id = 3

@app.route("/", methods=['GET'])
def hello():
    return "Hello world"


@app.route("/posts", methods=['GET'])
def get_posts():
    return jsonify(posts)

@app.route("/posts/<int:post_id>", methods=['GET'])
def get_post(post_id):
    post = next((p for p in posts if p["id"] == post_id), None)
    if post:
        time.sleep(random.uniform(0.1, 0.3))
        return jsonify(post)
    return jsonify({"error": "Post not found"}), 404

@app.route("/posts", methods=['POST'])
def create_post():
    global next_id
    if not request.json or not 'title' in request.json or not 'author' in request.json:
        return jsonify({"error": "Bad"}), 400

    time.sleep(random.uniform(0.5, 1.5))

    new_post = {
        "id": next_id,
        "author": request.json['author'],
        "title": request.json['title'],
        "content": request.json.get('content', "")
    }
    posts.append(new_post)
    next_id += 1
    return jsonify(new_post), 201

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)

