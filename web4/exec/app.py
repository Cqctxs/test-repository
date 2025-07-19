from flask import Flask, jsonify, request, render_template
from pymongo import MongoClient
from db import db_init
import os

FLAG = os.environ.get("FLAG", "wxmctf{dummy")
MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost")

db_init()

app = Flask(__name__)

client = MongoClient(MONGO_URI)

db = client["store"]
store_products = db["products"]

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/shop')
def shop():
    return render_template('shop.html')


@app.route("/api/products", methods=["GET"])
def get_available_products():
    products = store_products.find({'$where' : "this.is_published == 1"})

    formatted_products = []

    for product in products:
        formatted_product = {
            "name": product["name"],
            "description": product["description"],
            "price": product["price"],
            "image_link": product["image_link"],
            "is_available" : product["is_available"]
        }
        formatted_products.append(formatted_product)

    return jsonify(formatted_products)

@app.route("/api/categories", methods=["GET"])
def get_categories():
    
    categories = store_products.distinct("category")

    return jsonify(categories)

@app.route("/api/products/filter", methods=["POST"])
def filter_products():
    filter_params = request.json

    price_order = filter_params.get("price_order", None)
    category = filter_params.get("category", None)

    filter_query = {'$where' : f"this.category ==  '{category}' && this.is_published == 1"}

    filtered_products = store_products.find(filter_query).sort("price", -1 if price_order == "high_to_low" else 1)

    formatted_products = []

    for product in filtered_products:
        formatted_product = {
            "name": product["name"],
            "description": product["description"],
            "price": product["price"],
            "stock": product["stock"],
            "image_link": product["image_link"]
        }
        formatted_products.append(formatted_product)

    return jsonify(formatted_products)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=1337)
