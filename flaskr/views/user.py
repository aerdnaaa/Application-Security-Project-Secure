from flask import Blueprint, render_template, request, redirect, url_for, flash, session, make_response
from flaskr.forms import Register, SignIn, Forget, Recover, PaymentOptions
from flaskr import file_directory, mail
from flaskr.models.User import User
from flaskr.models.PaymentInfo import PaymentInfo
from flask_mail import Message
import sqlite3, os
import math, random
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

# HASH
import hashlib

# PASSWORD STRENGTH CHECKER
from password_strength import PasswordPolicy, PasswordStats

# FLASK LOGIN
from flask_login import current_user, login_user, logout_user, login_required

user_blueprint = Blueprint('user', __name__)


# ============================================= Sign in/ Register ===============================================#
@user_blueprint.route("/Register", methods=["GET", "POST"])
def register():
    try:
        current_user.get_username()
        return redirect(url_for('main.home'))
    except:
        user = None

    register = Register(request.form)
    if request.method == "POST" and register.validate():
        conn = sqlite3.connect(os.path.join(file_directory, "storage.db"))
        c = conn.cursor()
        if c.execute("SELECT username FROM users WHERE username= ? ", (register.username.data,)).fetchone() == None:
            # Password policy
            policy = PasswordPolicy.from_names(
                length=12,  # min length: 12
                uppercase=1,  # need min. 1 uppercase letters
                numbers=1,  # need min. 1 digits
                special=1,  # need min. 1 special characters
            )
            errorMsg = [] # List to store error messages
            
            # Checks password against policy and stores violations in list
            check = policy.test(register.password.data) 
            strengthLvl = PasswordStats(register.password.data).strength()
            # If password has 0 errors and meets complexity requirement, password hashed and stored in database
            if check == [] and  strengthLvl> 0.5:
                pw_hash = hashlib.sha256(register.password.data.encode()).hexdigest()
                c.execute("INSERT INTO users (username, email, password, admin) VALUES (?, ?, ?, ?)", (register.username.data, register.email.data, pw_hash, 'n'))
                conn.commit()
                conn.close()
                return redirect(url_for('user.signin'))

            else:
                # Goes through check list to check which policy does password fail
                for i in check:
                    if type(i).__name__ == 'Length':
                        errorMsg.append('Password must have a minimum of 12 characters')
                    elif type(i).__name__ == 'Uppercase':
                        errorMsg.append("Password must include uppercase characters")
                    elif type(i).__name__ == 'Numbers':
                        errorMsg.append("Password must include numbers")
                    elif type(i).__name__ == 'Special':
                        errorMsg.append("Password must include special characters (eg. !, @, #, $, %)")
                # Strength level checks complexity of password
                if strengthLvl < 0.5:
                    errorMsg.append("Password too simple. Avoid simple combinations and dictionary words")
                flash(errorMsg, 'password')
        else:
            # Flash error message if user exists
            flash('Username exists! Please try again', 'username')

    return render_template("user/Register.html", user=user, form=register)


@user_blueprint.route("/Signin", methods=["GET", "POST"])
def signin():
    # Checks if user is logged in
    try:
        current_user.get_username()
        return redirect(url_for('main.home'))
    except:
        user = None

    signin = SignIn(request.form)
    if request.method == "POST" and signin.validate():
        pw_hash = hashlib.sha256(signin.password.data.encode()).hexdigest()
        conn = sqlite3.connect(os.path.join(file_directory, "storage.db"))
        c = conn.cursor()
        c.execute("SELECT rowid, * FROM users WHERE username=? AND password=?", (signin.username.data, pw_hash))
        conn.commit()
        user = c.fetchone()

        # Patched code: Gives ambiguous error message
        if user == None:
            flash("Incorrect username or password")
        else:
            userObj = User(user[0], user[1], user[2], user[3], user[4])
            if userObj.get_admin() == 'y':
                login_user(userObj)
                return redirect(url_for('admin.admin'))
            else:
                login_user(userObj)
                return redirect(url_for('main.home'))

        conn.close()
    return render_template("user/SignIn.html", form=signin, user=user)


# FLASK LOGIN
@user_blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))


# ============================================= User Page =============================================#
# @user_blueprint.route("/Profile", methods=["GET", "POST"])
# def Profile():
#     if 'username' in session:
#         user = User(session['username'], session['email'], session['password'], session['question'], session['answer'])
#         # get payment information if have
#         conn = sqlite3.connect(os.path.join(file_directory, "storage.db"))
#         c = conn.cursor()
#         c.execute("SELECT * FROM paymentdetails WHERE username='{}' ".format(user.get_username()))
#         # self define paymentinformation and fetch one and return into payment information variable.
#         paymentinformation = c.fetchone()
#         # get all the 4 attribute from the PaymentInfo.py
#         if paymentinformation:
#             payment_details = PaymentInfo(paymentinformation[1], paymentinformation[2], paymentinformation[3],
#                                           int(paymentinformation[4]))
#         else:
#             payment_details = PaymentInfo("", "", "", "")
#     else:
#         return redirect(url_for('user.signin'))

#     payment_form = PaymentOptions(request.form)
#     if request.method == "POST" and payment_form.validate():
#         print("this code is running")
#         conn = sqlite3.connect(os.path.join(file_directory, "storage.db"))
#         c = conn.cursor()
#         c.execute("SELECT * FROM paymentdetails WHERE username='{}' ".format(user.get_username()))
#         result = c.fetchone()
#         if not result:
#             c.execute("INSERT INTO paymentdetails VALUES ('{}','{}','{}','{}','{}')".format(user.get_username(),
#                                                                                             payment_form.Name.data,
#                                                                                             payment_form.CreditCardno.data,
#                                                                                             payment_form.ExpiryDate.data,
#                                                                                             payment_form.SecretNumber.data))
#             conn.commit()
#             conn.close()
#             return redirect(url_for('user.Profile'))
#         else:
#             flash('Only can store 1 card detail')

#     return render_template("user/Profile.html", user=user, form=payment_form, payment_details=payment_details)

@user_blueprint.route("/Profile", methods=["GET", "POST"])
@login_required
def Profile():
    user = current_user
    return render_template("user/Profile.html", user=user)

@user_blueprint.route("/Forget", methods=["GET", "POST"])
def forget():
    try:
        current_user.get_username()
        return redirect(url_for('main.home'))
    except:
        user = None

    form = Forget(request.form)
    if request.method == "POST" and form.validate():
        conn = sqlite3.connect(os.path.join(file_directory, "storage.db"))
        c = conn.cursor()
        c.execute("SELECT username, email FROM users WHERE email=?", (form.email.data,))
        user = c.fetchone()
        if user != None:
            # Generate OTP
            digits = "0123456789"
            OTP = "" 
            for i in range(6) : 
                OTP += digits[math.floor(random.random() * 10)]

            # Generate Token
            s = Serializer('secret_key', 120)
            token = s.dumps(OTP).decode('UTF-8')
            c.execute("UPDATE users SET token=? WHERE username=?", (token, user[0]))
            conn.commit()

            # Send Email to user
            mail.send_message(
                'Indirect Home Gym Password Reset',
                sender='ballsnpaddles@gmail.com',
                recipients=[user[1]],
                body="Dear {}\n\nYour 6 digit OTP {} will expire in 2 minutes.\n\nRegards\nIndirect Home Gym Team".format(user[0], OTP)
            )
            return redirect(url_for('user.Reset', username=user[0]))
        else:
            flash("Email does not exist!")
                
    return render_template("user/Forget.html", user=user, form=form)

@user_blueprint.route("/Reset_Password/<username>", methods=["GET", "POST"])
def Reset(username):
    try:
        current_user.get_username()
        return redirect(url_for('main.home'))
    except:
        user = None

    form = Recover(request.form)
    if request.method == "POST" and form.validate():
        conn = sqlite3.connect(os.path.join(file_directory, "storage.db"))
        c = conn.cursor()
        c.execute("SELECT token FROM users WHERE username=?", (username,))
        token = c.fetchone()[0]
        s = Serializer('secret_key', 120)
        try:
            s.loads(token)
        except:
            flash("Your OTP has Expired")

    return render_template("user/Recover.html", user=user, form=form)

@user_blueprint.route("/Voucher")
def Voucher():
    try:
        current_user.get_username()
        user = current_user
    except:
        return redirect(url_for('user.signin'))

    return render_template("user/Voucher.html", title="Vouchers", user=user)
