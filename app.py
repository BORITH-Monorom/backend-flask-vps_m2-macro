# app.py
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
# Use a different database for testing/development
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    content = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f'<Post {self.title}>'

@app.route('/')
def hello_world():
    return 'Hello, World! This is my Flask app with SQLAlchemy.'

@app.route('/posts', methods=['POST'])
def create_post():
    data = request.get_json()
    new_post = Post(title=data['title'], content=data['content'])
    db.session.add(new_post)
    db.session.commit()
    return jsonify({'message': 'Post created!'}), 201

@app.route('/posts', methods=['GET'])
def get_posts():
    posts = Post.query.all()
    posts_list = []
    for post in posts:
        posts_list.append({
            'id': post.id,
            'title': post.title,
            'content': post.content
        })
    return jsonify(posts_list)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)