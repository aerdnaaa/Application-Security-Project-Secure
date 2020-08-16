import os
import requests
import sqlite3

from flask import Blueprint, render_template, session, request, redirect, url_for, abort
from flask_login import current_user
from flaskr import file_directory
from flaskr.forms import SearchForm

shopping_blueprint = Blueprint('shopping', __name__)


@shopping_blueprint.route("/ShoppingCart", methods=["GET", "POST"])
def ShoppingCart():
    try:
        current_user.get_username()
        user = current_user
    except:
        user = None

    original_cost = 0

    if 'cart' in session:
        cart = session['cart']
        for item in cart:
            original_cost += item[4]
    else:
        cart = []

    result_cost = original_cost

    if 'voucher' in session:
        voucher_code = session['voucher']
        conn = sqlite3.connect(os.path.join(file_directory, "storage.db"))
        c = conn.cursor()
        c.execute("SELECT amount from vouchers where code=? ", (voucher_code,))
        amount = c.fetchone()
        result_cost -= amount[0]
    else:
        voucher_code = ""

    return render_template("shopping/ShoppingCart.html", user=user, cart=cart, original_cost=original_cost,
                           result_cost=result_cost, voucher_code=voucher_code)


@shopping_blueprint.route("/apply_voucher/<voucher_code>")
def apply_voucher(voucher_code):
    if '_user_id' in session and voucher_code != ":":
        session['voucher'] = voucher_code
    elif 'voucher' in session:
        del session['voucher']

    return redirect(url_for('shopping.ShoppingCart'))


@shopping_blueprint.route("/checkout")
def checkout():
    try:
        current_user.get_username()
        user = current_user
    except:
        user = None

    # Check if cart is in session or empty
    if 'cart' in session:
        cart = session['cart']
        if not cart:
            return redirect(url_for('main.home'))
    else:
        return redirect(url_for('main.home'))

    # uses the voucher
    if '_user_id' in session and 'voucher' in session:
        cookie = request.headers['cookie']
        headers = {'cookie': cookie}
        url = "http://localhost:5000/api/userVoucher/" + session["_user_id"]
        response = requests.put(url, json={"code": session["voucher"]}, headers=headers)

        data = response.json()["data"]
        if data == "This is a general voucher":
            data = ""
    else:
        data = ""

    del session['cart']
    if 'voucher' in session:
        del session['voucher']
    return render_template("shopping/Checkout.html", data=data, user=user)


@shopping_blueprint.route("/Add/<product_id>")
def addToCart(product_id):
    if 'cart' in session:
        cart = session['cart']
    else:
        cart = []

    conn = sqlite3.connect(os.path.join(file_directory, "storage.db"))
    c = conn.cursor()
    c.execute(" SELECT * FROM products WHERE product_id=? ", product_id)
    item = c.fetchone()
    # Check if product is inactive
    # If product not active, display error 404 page
    if item is None or item[6] == "inactive":
        abort(404)
    else:
        cart.append(item)
        session['cart'] = cart

    return redirect(url_for('shopping.ShoppingCart'))


@shopping_blueprint.route("/Products", methods=['POST', 'GET'])
def Products():
    try:
        current_user.get_username()
        user = current_user
    except:
        user = None

    conn = sqlite3.connect(os.path.join(file_directory, "storage.db"))
    c = conn.cursor()

    c.execute("SELECT * FROM products")
    products = c.fetchall()
    conn.close()

    search = SearchForm(request.form)
    if request.method == "POST":
        return redirect(url_for('shopping.Search', product=search.Search.data))

    return render_template("shopping/Products.html", user=user, form=search, products=products)


@shopping_blueprint.route("/Search/<product>", methods=['POST', 'GET'])
def Search(product):
    try:
        current_user.get_username()
        user = current_user
    except:
        user = None

    # For search
    conn = sqlite3.connect(os.path.join(file_directory, "storage.db"))
    c = conn.cursor()
    c.execute("SELECT rowid, * FROM products WHERE name=? ", (product,))
    results = c.fetchall()
    conn.close()

    # Search Form
    form = SearchForm(request.form)
    if request.method == "POST":
        return redirect(url_for('shopping.Search', product=form.Search.data))

    return render_template("shopping/Search.html", user=user, products=results, search=product, form=form)


@shopping_blueprint.route("/Vouchers")
def vouchers():
    try:
        current_user.get_username()
        user = current_user
    except:
        user = None

    return render_template("shopping/Vouchers.html", user=user)
