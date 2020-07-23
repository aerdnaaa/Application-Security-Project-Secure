from wtforms import Form, StringField, TextAreaField, IntegerField, FileField, RadioField, FloatField, validators, PasswordField, SelectField, BooleanField, SubmitField
from wtforms.fields.html5 import EmailField, DateField
import datetime


class Register(Form):
    username = StringField("Username", [validators.InputRequired(), validators.Length(min=1, max=150)])
    email = EmailField("Email", [validators.InputRequired(), validators.Email()])
    password = PasswordField("Password", [validators.InputRequired()])
    question = SelectField('Secruity Question', [validators.DataRequired()], choices=
                [("What is the middle name of your mother?", "What is the middle name of your mother?"),
                ("What is the name of your pet?", "What is the name of your pet?"), 
                ("What is the first thing you learnt to cook?", "What is the first thing you learnt to cook?"),
                ("What was the first film you saw in cinema?", "What was the first film you saw in cinema?"),
                ("Where was the first place you went to on a plane?", "Where was the first place you went to on a plane?"),
                ("What is the name of your favourite teacher?", "What is the name of your favourite teacher?")], 
                default="What is the middle name of your mother?")
    answer = StringField("Answer", [validators.InputRequired()])


class SignIn(Form):
    username = StringField("Username", [validators.InputRequired()])
    password = PasswordField("Password", [validators.InputRequired()])

class Forget(Form):
    username = StringField("Username", [validators.InputRequired()])

class Recover(Form):
    answer = StringField("Answer", [validators.InputRequired()])
    password = PasswordField("New Password", [validators.InputRequired()])

class ContactUs(Form):
    name = StringField('Name', [validators.Length(max=50), validators.InputRequired()])
    email = EmailField('Email Address', [validators.Email(), validators.InputRequired()])
    subject = StringField('Subject', [validators.Length(min=1, max=150), validators.InputRequired()])
    message = TextAreaField('Messsage', [validators.InputRequired()])


class SearchForm(Form):
    Search = StringField("", [validators.Optional()])

class PaymentOptions(Form):
    Name = StringField("Full Name", [validators.InputRequired()])
    CreditCardno = StringField("Credit Card Number", [validators.Length(min=16, max=16)])
    ExpiryDate = DateField("Expiry Date",[validators.InputRequired()], format='%Y-%m-%d')
    SecretNumber = PasswordField("CCV", [validators.Length(min=3,max=3)])

class Reviews(Form):
    reviews = StringField("Reviews", [validators.InputRequired()])



