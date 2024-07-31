from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, EmailField
from wtforms.validators import DataRequired, URL, Email
from flask_ckeditor import CKEditorField


class CreateCafe(FlaskForm):
    name = StringField("Name:", validators=[DataRequired()])
    map_url = StringField("Map URL", validators=[URL()])
    