from flask import Blueprint, render_template, request, redirect, url_for, flash, session, make_response
from flaskr.forms import Register, SignIn, Forget, PaymentOptions, Reset
from flaskr import file_directory, mail
from flaskr.models.User import User
from flaskr.models.PaymentInfo import PaymentInfo
import pyffx
from flask_mail import Message
import sqlite3, os
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
            errorMsg = []  # List to store error messages

            # Checks password against policy and stores violations in list
            check = policy.test(register.password.data)
            strengthLvl = PasswordStats(register.password.data).strength()
            # If password has 0 errors and meets complexity requirement, password hashed and stored in database
            if check == [] and strengthLvl > 0.5:
                pw_hash = hashlib.sha512(register.password.data.encode()).hexdigest()
                c.execute("INSERT INTO users VALUES (?, ?, ?, ?)",
                          (register.username.data, register.email.data, pw_hash, 'n'))
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
        pw_hash = hashlib.sha512(signin.password.data.encode()).hexdigest()
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
#
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
#
#     return render_template("user/Profile.html", user=user, form=payment_form, payment_details=payment_details)

@user_blueprint.route("/Profile", methods=["GET", "POST"])
@login_required
def Profile():
    user = current_user
    conn = sqlite3.connect(os.path.join(file_directory, "storage.db"))
    c = conn.cursor()
    c.execute("SELECT * FROM paymentdetails WHERE username='{}' ".format(user.get_username()))
    # self define paymentinformation and fetch one and return into payment information variable.
    paymentinformation = c.fetchone()
    if paymentinformation:
        payment_details = PaymentInfo(paymentinformation[1], paymentinformation[2], paymentinformation[3],
                                      int(paymentinformation[4]))
    else:
        payment_details = PaymentInfo("", "", "", "")

    payment_form = PaymentOptions(request.form)
    if request.method == "POST" and payment_form.validate():
        conn = sqlite3.connect(os.path.join(file_directory, "storage.db"))
        c = conn.cursor()
        c.execute("SELECT * FROM paymentdetails WHERE username='{}' ".format(user.get_username()))
        result = c.fetchone()
        if not result:
            e1 = pyffx.Integer(b'12376987ca98sbdacsbjkdwd898216jasdnsd98213912', length=16)
            e2 = pyffx.Integer(b'12376987ca98sbdacsbjkdwd898216jasdnsd98213912',
                               length=len(str(payment_form.SecretNumber.data)))
            encrypted_card_no = e1.encrypt(payment_form.CreditCardno.data)
            encrypted_card_CVV = e2.encrypt(payment_form.SecretNumber.data)
            c.execute("INSERT INTO paymentdetails VALUES ('{}','{}','{}','{}','{}')".format(user.get_username(),
                                                                                            payment_form.Name.data,
                                                                                            encrypted_card_no,
                                                                                            payment_form.ExpiryDate.data,
                                                                                            encrypted_card_CVV))
            conn.commit()
            conn.close()
            return redirect(url_for('user.Profile'))
        else:
            flash('Only can store 1 card detail')
    if payment_details.get_full_name() != '':
        cn = payment_details.get_credit_card_number()
        e1 = pyffx.Integer(b'12376987ca98sbdacsbjkdwd898216jasdnsd98213912', length=16)
        cn = e1.decrypt(cn)
        return render_template("user/Profile.html", user=user, payment_details=payment_details, form=payment_form,
                               cn=str(cn))
    return render_template("user/Profile.html", user=user, payment_details=payment_details, form=payment_form)


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
        userInfo = c.fetchone()
        if userInfo != None:
            # Generate Token
            s = Serializer('secret_key', 300)

            # Store username in token for authentication
            token = s.dumps(userInfo[0]).decode('UTF-8')

            # Send Email to user
            mail.send_message(
                'Indirect Home Gym Password Reset',
                sender='ballsnpaddles@gmail.com',
                recipients=[userInfo[1]],
                body="Hi {},\n\nYou recently requested to reset your password for your account. Click on the link below to change your password\n\n http://127.0.0.1:5000/Reset_Password/{} \n\n If you did not request a password reset, please ignore this email or reply to us to let us know. This link is only valid for the next 5 minutes.\n\nCheers!\nIndirect Home Gym Team".format(
                    userInfo[0], token)
            )

            flash("A password reset link has been sent to your email!", "success")
        else:
            flash("Email does not exist!", "danger")

    return render_template("user/Forget.html", user=user, form=form)


@user_blueprint.route("/Reset_Password/<token>", methods=["GET", "POST"])
def reset(token):
    try:
        current_user.get_username()
        return redirect(url_for('main.home'))
    except:
        user = None

    try:
        # Check if token is valid
        s = Serializer('secret_key', 300)
        username = s.loads(token)
        valid = True
    except:
        valid = False

    form = Reset(request.form)
    if request.method == "POST" and form.validate():
        conn = sqlite3.connect(os.path.join(file_directory, "storage.db"))
        c = conn.cursor()
        # Password policy
        policy = PasswordPolicy.from_names(
            length=12,  # min length: 12
            uppercase=1,  # need min. 1 uppercase letters
            numbers=1,  # need min. 1 digits
            special=1,  # need min. 1 special characters
        )
        errorMsg = []  # List to store error messages

        # Checks password against policy and stores violations in list
        check = policy.test(form.password.data)
        strengthLvl = PasswordStats(form.password.data).strength()
        # If password has 0 errors and meets complexity requirement, password hashed and stored in database
        if check == [] and strengthLvl > 0.5:
            pw_hash = hashlib.sha512(form.password.data.encode()).hexdigest()
            c.execute("UPDATE users SET password=? WHERE username=?", (pw_hash, username))
            conn.commit()
            conn.close()
            flash("Your password has been changed!", "success")

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

    return render_template("user/Reset.html", user=user, form=form, valid=valid)
