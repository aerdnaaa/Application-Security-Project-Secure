from flask import Blueprint, render_template, request, redirect, url_for, flash, session, make_response
from flaskr.models.User import User
from flaskr.forms import ContactUs, Reviews
import sqlite3, os
from flaskr import file_directory

main_blueprint = Blueprint('main', __name__)


@main_blueprint.route("/")
@main_blueprint.route("/Home")
def home():
    if 'username' in session:
        user = User(session['username'], session['email'], session['password'], session['question'], session['answer'])
    else:
        user = None
    
    conn = sqlite3.connect(os.path.join(file_directory, "storage.db"))
    c = conn.cursor()

    c.execute("SELECT rowid, * FROM products")
    products = c.fetchall()
    conn.close()

    return render_template("main/Home.html", user=user, products=products)


@main_blueprint.route("/About")
def About():
    if 'username' in session:
        user = User(session['username'], session['email'], session['password'], session['question'], session['answer'])
    else:
        user = None
    
    conn = sqlite3.connect(os.path.join(file_directory, "storage.db"))
    c = conn.cursor()

    c.execute("SELECT * FROM reviews WHERE productid=4")
    product = c.fetchone()
    conn.close()

    return render_template("main/About.html", user=user, product=product)


@main_blueprint.route("/FAQ")
def FAQ():
    if 'username' in session:
        user = User(session['username'], session['email'], session['password'], session['question'], session['answer'])
    else:
        user = None

    return render_template("main/FAQ.html", user=user)


@main_blueprint.route("/Emailus", methods=["GET", "POST"])
def emailus():
    if 'username' in session:
        user = User(session['username'], session['email'], session['password'], session['question'], session['answer'])
    else:
        user = None
    contactUsForm = ContactUs(request.form)
    conn = sqlite3.connect(os.path.join(file_directory, "storage.db"))
    c = conn.cursor()
    if request.method == "POST" and contactUsForm.validate():
        
        c.execute("""INSERT INTO query VALUES ("{}", "{}", "{}","{}")""".format(contactUsForm.name.data,contactUsForm.email.data,contactUsForm.subject.data,contactUsForm.message.data)) 
        conn.commit()
        conn.close()
        return redirect(url_for('main.emailus'))
    return render_template("main/Emailus.html", user=user, form=contactUsForm)

@main_blueprint.route("/Reviews/<productid>", methods=["GET", "POST"])
def reviews(productid):
    if 'username' in session:
        user = User(session['username'], session['email'], session['password'], session['question'], session['answer'])
    else:
        user = None

    reviewsform = Reviews(request.form)
    conn = sqlite3.connect(os.path.join(file_directory, "storage.db"))
    c = conn.cursor()
    c.execute("SELECT rowid,* FROM products WHERE rowid={}".format(productid))
    product = c.fetchone()

    c.execute("SELECT * FROM reviews")
    reviews=c.fetchall()

    if request.method == "POST" and reviewsform.validate():
        c.execute("""INSERT INTO reviews VALUES ("{}", "{}", "{}")""".format(product[0], user.get_username(), reviewsform.reviews.data)) 
        conn.commit()
        return redirect(url_for('main.reviews', productid=productid))
    
    return render_template("main/Reviews.html", user=user, product=product, reviews=reviews, form=reviewsform)
