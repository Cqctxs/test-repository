from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017/')
db = client.mydb

@app.route('/posts')
def get_posts():
    # Accept only certain fields for filtering
    author = request.args.get('author')
    tag = request.args.get('tag')

    query = {}
    if author:
        # Enforce that author is plain string, no $where
        query['author'] = author
    if tag:
        query['tags'] = tag

    posts = list(db.posts.find(query, {'_id': 0, 'title': 1, 'author': 1, 'tags': 1}))
    return jsonify(posts)

@app.route('/post/<post_id>')
def get_post(post_id):
    try:
        obj_id = ObjectId(post_id)
    except Exception:
        return jsonify({'error': 'Invalid post id'}), 400
    post = db.posts.find_one({'_id': obj_id}, {'_id': 0})
    if post:
        return jsonify(post)
    return jsonify({'error': 'Not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)