import psycopg2
from flask import Flask, request, jsonify

app = Flask(__name__)

def get_db_connection():
    return psycopg2.connect(
        dbname="appdb",
        user="appuser",
        password="secret",
        host="localhost"
    )

@app.route('/product', methods=['GET'])
def get_product():
    prod_id = request.args.get('id')
    # Validate and cast to integer
    try:
        prod_id_int = int(prod_id)
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid ID"}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    # Parameterized query to prevent SQL injection
    cur.execute(
        'SELECT id, name, price FROM products WHERE id = %s',
        (prod_id_int,)
    )
    row = cur.fetchone()
    conn.close()

    if row:
        product = {"id": row[0], "name": row[1], "price": float(row[2])}
        return jsonify(product), 200
    else:
        return jsonify({"error": "Product not found"}), 404

if __name__ == '__main__':
    app.run()