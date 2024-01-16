from dotenv import load_dotenv
load_dotenv()

import os

mongo_uri = os.getenv('MONGO_URI')

from pymongo import MongoClient

client = MongoClient(mongo_uri)
db = client.db_jungle

from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/books/list", methods=['GET'])
def show_books():
    all_books = list(db.books.find({},{"_id": False}).sort("like", -1))
    return jsonify({
        "result": "succcess", 
        "all_books": all_books
        })

@app.route("/api/books/like", methods=['POST'])
def like_book():
    return jsonify({"result": "succcess", "msg": "like 연결되었습니다"})

@app.route("/api/books/delete", methods=['POST'])
def delete_book():
    return jsonify({"result": "succcess", "msg": "delete 연결되었습니다"})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)