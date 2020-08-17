import os
import pyffx
import sqlite3
from datetime import datetime
import requests

from flask import Blueprint, render_template, session, request, redirect, url_for, abort
from flask_login import current_user
from flaskr import file_directory
from flaskr.forms import SearchForm
from flaskr.services.loggingservice import Logging

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
        if session['voucher'] != "":
            voucher_code = session['voucher']
            conn = sqlite3.connect(os.path.join(file_directory, "storage.db"))
            c = conn.cursor()
            c.execute("SELECT amount from vouchers where code=? ", (voucher_code,))
            amount = c.fetchone()
            result_cost -= amount[0]
        else:
            voucher_code = ""
            session['voucher'] = ""
    else:
        voucher_code = ""
        session['voucher'] = ""

    session["subtotal"] = original_cost
    session['amount'] = result_cost

    return render_template("shopping/ShoppingCart.html", user=user, cart=cart, original_cost=original_cost,
                           result_cost=result_cost, voucher_code=voucher_code)


@shopping_blueprint.route("/apply_voucher/<voucher_code>")
def apply_voucher(voucher_code):
    if voucher_code != ":":
        # check if voucher is general voucher
        conn = sqlite3.connect(os.path.join(file_directory, "storage.db"))
        c = conn.cursor()
        c.execute("SELECT user_id from vouchers where code = ?", (voucher_code,))
        user_id = c.fetchone()[0]
        if user_id == 0:
            # voucher used is general
            session['voucher'] = voucher_code
        elif str(user_id) == str(session["_user_id"]):
            # voucher belongs to user with the current session
            session['voucher'] = voucher_code
    # delete voucher if voucher selected is empty
    elif 'voucher' in session and voucher_code == ":":
        del session['voucher']

    return redirect(url_for('shopping.ShoppingCart'))


@shopping_blueprint.route("/checkout", methods=["GET", "POST"])
def checkout():
    try:
        username = current_user.get_username()
        user = current_user
        user_id = session["_user_id"]
    except:
        user = None
        user_id = None
    error = ""

    # Check if cart is in session or empty
    if 'cart' in session:
        cart = session['cart']
        if not cart:
            return redirect(url_for('main.home'))
    else:
        return redirect(url_for('main.home'))
    # if user is not signin, will redirect to ask to signin
    if not user:
        return redirect(url_for('user.signin'))
    else:
        # getting card from existing user
        conn = sqlite3.connect(os.path.join(file_directory, "storage.db"))
        c = conn.cursor()
        c.execute("SELECT credit_card_number from paymentdetails where user_id=?", (user_id,))
        result = c.fetchone()
        if result:
            e1 = pyffx.Integer(b'12376987ca98sbdacsbjkdwd898216jasdnsd98213912', length=16)
            credit_card_number = str(e1.decrypt(result[0]))
            sliced_credit_card_number = "XXXX-" * 3 + credit_card_number[-4:]
        else:
            return redirect(url_for('user.Profile'))

    # payment
    if request.method == "POST" and user is not None:
        month = request.form.get('Expiry_DateM')
        year = request.form.get('Expiry_DateY')
        cvv = request.form.get('CVV')
        # validate credit card details
        conn = sqlite3.connect(os.path.join(file_directory, "storage.db"))
        c = conn.cursor()
        c.execute("SELECT expiry, cvv, credit_card_number from paymentdetails where user_id=?", (user_id,))
        result = c.fetchone()
        valid_year, valid_month, valid_day = result[0].split('-')
        e2 = pyffx.Integer(b'12376987ca98sbdacsbjkdwd898216jasdnsd98213912', length=len(str(result[1])))
        valid_cvv = e2.decrypt(result[1])
        print(cvv)
        if int(year) == int(valid_year[2:]) and int(month) == int(valid_month) and str(cvv) == str(valid_cvv):
            # successful payment
            c.execute("select max(order_id) from orders")
            try:
                order_id = c.fetchone()[0] + 1
            except TypeError:
                order_id = 1
            user_id = session["_user_id"]
            voucher_code = session["voucher"]
            date_of_purchase = datetime.now()
            total_cost = session["amount"]

            c.execute("INSERT into orders values (?, ?, ?, ?, ?)",
                      (order_id, user_id, voucher_code, date_of_purchase, total_cost))
            for item in session['cart']:
                c.execute("INSERT into order_details values (?,?)", (order_id, item[0]))
            conn.commit()
            conn.close()

            # uses the voucher (should only use it after payment is successful)
            if '_user_id' in session and 'voucher' in session and session['voucher'] != '':
                cookie = request.headers['cookie']
                headers = {'cookie': cookie}
                url = "http://localhost:5000/api/userVoucher/" + session["_user_id"]
                response = requests.put(url, json={"code": session["voucher"]}, headers=headers)

                data = response.json()["data"]
                if data == "This is a general voucher":
                    data = ""
            else:
                data = ""

            # deletes voucher and cart session
            del session['cart']
            if 'voucher' in session:
                del session['voucher']

            return render_template("shopping/Thankyou.html", data=data, user=user)

        else:
            # unsuccessful payment
            details = f"Failed transaction with the username of {username}."
            Loggingtype = "Transaction"
            Logging(Loggingtype, details)
            error = "Invalid Payment Details"

    # checkout details
    cart = session['cart']
    voucher = session['voucher']
    conn = sqlite3.connect(os.path.join(file_directory, "storage.db"))
    c = conn.cursor()
    c.execute("SELECT amount from vouchers where code = ?", (voucher,))
    try:
        voucher_cost = c.fetchone()[0]
    except TypeError:
        voucher_cost = 0
    subtotal = session['subtotal']
    amount = session['amount']
    order_details = {
        'cart': cart,
        'voucher': voucher,
        'voucher_cost': voucher_cost,
        'subtotal': subtotal,
        'total': amount
    }

    return render_template("shopping/Checkout.html", user=user, credit_card_number=sliced_credit_card_number, error_message=error, order_details=order_details)


@shopping_blueprint.route("/Add/<product_id>")
def addToCart(product_id):
    try:
        current_user.get_username()
    except:
        return redirect(url_for('user.signin'))

    if 'cart' in session:
        cart = session['cart']
    else:
        cart = []

    conn = sqlite3.connect(os.path.join(file_directory, "storage.db"))
    c = conn.cursor()
    c.execute(" SELECT product_id, name, image, description, selling_price, category, status FROM products WHERE product_id=? ", (product_id,))
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
