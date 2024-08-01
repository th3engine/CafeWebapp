from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, EmailField, RadioField
from wtforms.validators import DataRequired, URL, Email
from flask_ckeditor import CKEditorField


class CreateCafe(FlaskForm):
    name = StringField("Name:", validators=[DataRequired()])
    map_url = StringField("Map URL", validators=[URL(),DataRequired()])
    img_url = StringField("Image URL", validators=[URL(),DataRequired()])
    location = StringField("Location",validators=[DataRequired()])
    has_wifi = RadioField("Does the venue have free Wi-fi?",validators=[DataRequired()],choices=[(True,"Yes"),(False,"No")])
    has_sockets = RadioField("Does the venue have sockets?",validators=[DataRequired()],choices=[(True,"Yes"),(False,"No")])
    has_toilet = RadioField("Does the venue have toilets?",validators=[DataRequired()],choices=[(True,"Yes"),(False,"No")])
    can_take_calls = RadioField("Are you able to take calls in this venue?",validators=[DataRequired()],choices=[(True,"Yes"),(False,"No")])
    seats = StringField("What is the number of seats roughly? (Can be a range)", validators=[DataRequired()])
    coffee_price = StringField("What is the average price of coffee here?",validators=[DataRequired()])
    submit = SubmitField("Add to database")


class UserLogin(FlaskForm):
    email = EmailField("Email: ", validators=[DataRequired(),Email()])
    password = PasswordField("Password",validators=(DataRequired()))

class RegisterUser(FlaskForm):
    first_name = StringField("First Name: ", validators=[DataRequired()])
    email = EmailField("Email: ",validators=[DataRequired(),Email()])
    password = PasswordField("Password: ",validators=[DataRequired()])
    conf_password = PasswordField("Password: ", validators=[DataRequired()])