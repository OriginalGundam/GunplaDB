#search_routes.py

#Searching/filtering

from flask import Blueprint, request, jsonify

from database import get_connection


search_routes = Blueprint("search_routes", __name__)


@search_routes.route("/search", methods=["GET"])
def search_gunpla():

    name = request.args.get("name")
    grade = request.args.get("grade")
    category = request.args.get("category")
    status = request.args.get("status")
    p_bandai = request.args.get("p_bandai")
    variant = request.args.get("variant")

    connection = get_connection()
    cursor = connection.cursor()

    query = """
        SELECT *
        FROM gunpla
        WHERE 1=1
    """

    parameters = []

    if name:
        query += " AND name ILIKE %s"
        parameters.append(f"%{name}%")

    if grade:
        query += " AND grade = %s"
        parameters.append(grade)

    if category:
        query += " AND category = %s"
        parameters.append(category)

    if status:
        query += " AND status = %s"
        parameters.append(status)

    if p_bandai is not None:
        query += " AND p_bandai = %s"
        parameters.append(p_bandai.lower() == "true")

    if variant is not None:
        query += " AND variant = %s"
        parameters.append(variant.lower() == "true")

    query += " ORDER BY name ASC"

    cursor.execute(query, parameters)

    results = cursor.fetchall()

    cursor.close()
    connection.close()

    gunpla = []

    for kit in results:

        gunpla.append({
            "id": kit[0],
            "name": kit[1],
            "grade": kit[2],
            "category": kit[3],
            "p_bandai": kit[4],
            "variant": kit[5],
            "status": kit[6]
        })

    return jsonify(gunpla)


@search_routes.route("/gunpla/<int:gunpla_id>", methods=["GET"])
def get_gunpla(gunpla_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            name,
            grade,
            category,
            p_bandai,
            variant,
            status
        FROM gunpla
        WHERE id = %s;
    """, (gunpla_id,))

    kit = cursor.fetchone()

    if kit is None:
        cursor.close()
        connection.close()

        return jsonify({
            "error": "Gunpla not found."
        }), 404

    cursor.execute("""
        SELECT
            stores.name,
            stores.shipping_fee,
            price_history.price,
            price_history.availability,
            price_history.stock,
            price_history.product_url,
            price_history.updated_at
        FROM price_history
        JOIN stores
            ON price_history.store_id = stores.id
        WHERE price_history.gunpla_id = %s
        ORDER BY CASE
            UPPER(TRIM(price_history.availability))
                WHEN 'IN STOCK' THEN 1
                WHEN 'PRE-ORDER' THEN 2
                WHEN 'OUT OF STOCK' THEN 3
                ELSE 4
            END,
            price_history.price ASC;
    """, (gunpla_id,))

    prices = cursor.fetchall()

    cursor.close()
    connection.close()

    price_list = []

    for price in prices:
        price_list.append({
            "store": price[0],
            "shipping_fee": (
                float(price[1])
                if price[1] is not None
                else None
            ),
            "price": float(price[2]),
            "availability": price[3],
            "stock": price[4],
            "product_url": price[5],
            "updated_at": price[6]
        })

    return jsonify({
        "id": kit[0],
        "name": kit[1],
        "grade": kit[2],
        "category": kit[3],
        "p_bandai": kit[4],
        "variant": kit[5],
        "status": kit[6],
        "prices": price_list
    })


@search_routes.route("/stores", methods=["GET"])
def get_stores():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            name,
            website,
            marketplace,
            reliability,
            shipping_fee
        FROM stores
        ORDER BY name ASC;
    """)

    results = cursor.fetchall()

    cursor.close()
    connection.close()

    stores = []

    for store in results:

        stores.append({
            "id": store[0],
            "name": store[1],
            "website": store[2],
            "marketplace": store[3],
            "reliability": store[4],
            "shipping_fee": (
                float(store[5])
                if store[5] is not None
                else None
            )
        })

    return jsonify(stores)