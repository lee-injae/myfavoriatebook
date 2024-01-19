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
    all_books = list(
        db.books.find(
            {},{"_id": False})
            .sort("like", -1))
    return jsonify({
        "result": "success", 
        "all_books": all_books
    })

@app.route("/api/books/like", methods=['POST'])
def like_book():
    data = request.json
    title_receive = data.get("title_give")
    book = db.books.find_one({"title": title_receive})
    new_like = book["like"] + 1
    db.books.update_one(
        {"title": title_receive}, 
        {"$set" : {"like": new_like}}
        )    
    return jsonify(
        {"result": "success", 
         "msg": "liked!"}
         )

@app.route("/api/books/delete", methods=['DELETE'])
def delete_book():
    data = request.json
    title_receive = data.get("title_give")
    db.books.delete_one(
        {"title": title_receive}
        )
    return jsonify(
        {"result": "success", 
         "msg": "deleted!"}
         )

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)