import psycopg2
from flask import Flask, request, jsonify

app = Flask(__name__)

conn_params = {
    'dbname': 'mydb',
    'user': 'myuser',
    'password': 'mypassword',
    'host': 'localhost'
}

@app.route('/products')
def list_products():
    category = request.args.get('category', '').strip()
    if not category:
        return jsonify({'error': 'Category required'}), 400

    # Use parameterized query to prevent SQL injection
    with psycopg2.connect(**conn_params) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, name, price FROM products WHERE category = %s",
                (category,)
            )
            rows = cur.fetchall()
    products = [{'id': r[0], 'name': r[1], 'price': r[2]} for r in rows]
    return jsonify(products)

if __name__ == '__main__':
    app.run(debug=False)
