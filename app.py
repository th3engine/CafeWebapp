from flask import Flask,request, render_template, redirect, flash
from db import db, Cafe, User
from flask_bootstrap import Bootstrap5
from forms import RegisterUser, UserLogin, CreateCafe
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer
from functools import wraps
import os
from datetime import datetime as dt
from email_verification import generate_token, confirm_token, send_email

from dotenv import load_dotenv; load_dotenv()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]=os.getenv("DATABASE_URI")
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
app.config['SECURITY_PASSWORD_SALT'] = os.getenv("SECURITY_PASSWORD_SALT")

Bootstrap5(app)

db.init_app(app)
with app.app_context():
    db.create_all()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "/login"

@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User,user_id)

def logout_required(function):
    @wraps(function)
    def decorated(*args,**kwargs):
        if current_user.is_authenticated:
            return redirect('/')
        else:
            return function(*args,**kwargs)
    return decorated

def confirmation_required(function):
    @wraps(function)
    def decorated(*args,**kwargs):
        if current_user.confirmed:
            return function(*args,**kwargs)
        else:
            return render_template("confirm_registration.html")
    return decorated

@app.route("/")
def home():

    return render_template('index.html')

@app.route("/cafes")
def get_all_cafes():
    cafes = db.session.execute(db.select(Cafe).order_by(Cafe.name)).scalars()

    return render_template('all_cafes.html',cafes = cafes)

@app.route("/cafes/<int:cafe_id>")
def get_cafe(cafe_id):
    cafe = db.get_or_404(Cafe,cafe_id)

    return render_template('cafe.html', cafe=cafe)

@app.route("/register",methods=["GET","POST"])
@logout_required
def register_user():
    form = RegisterUser()

    if form.validate_on_submit():
        user_exists = db.session.execute(db.select(User).where(User.email==form.email.data)).scalar()
        if user_exists:
            flash("User with this email already exists. Please log in")
            return redirect("/login")
        else:
            new_user = User(
                name = form.first_name.data,
                email = form.email.data,
                password = generate_password_hash(form.password.data,method="scrypt:32768:8:1"),
                created_on = dt.now().replace(microsecond=0),
            )
            db.session.add(new_user)
            db.session.commit()
            token = generate_token(form.email.data)
            flash("You have successfully registered. Please confirm your email address before logging in",'info')
            send_email(token)
            return redirect("/login")

    return render_template("register.html",form = form)

@app.route('/register/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        flash("Account already confirmed","info")
        return redirect('/cafes')
    email = confirm_token(token)
    user = db.session.execute(db.select(User).where(User.email==current_user.email)).scalar()
    if user.email == email:
        user.confirmed = True
        user.confirmed_on = dt.now().replace(microsecond=0)
        db.session.add(user)
        db.session.commit()
        flash("You have successsfully confirmed your account","success")
        return redirect('/cafes')
    else:
        message = "The confirmation link is invalid or expired"
        return render_template("confirm_registration.html", message = message)

@app.route('/login',methods=["GET","POST"])
@logout_required
def login():
    form = UserLogin()
    if form.validate_on_submit():
        user = db.session.execute(db.select(User).where(User.email==form.email.data)).scalar()
        if user is not None and check_password_hash(user.password,form.password.data):
            login_user(user)
            return redirect("/")
        else:
            flash("Incorrect credentials",'danger')
            return redirect("/login")
        
    return render_template('login.html', form = form)

@app.route('/addcafe',methods=["GET","POST"])
@confirmation_required
@login_required
def add_cafe():
    form = CreateCafe()
    if form.validate_on_submit():
        data = form.data
        data.pop('submit',None)
        data.pop('csrf_token',None)
        new_cafe = Cafe(**data)
        db.session.add(new_cafe)
        db.session.commit()
        flash(f"{data.get('name')} successfully added",'success')
        return redirect('/cafes')
    return render_template('add_cafe.html',form=form)


@app.route('/editcafe/<int:cafe_id>',methods=["GET","POST"])
@confirmation_required
@login_required
def edit_cafe(cafe_id):
    cafe = db.get_or_404(Cafe,cafe_id)
    form = CreateCafe(
        name = cafe.name,
        map_url = cafe.map_url,
        img_url = cafe.img_url,
        location = cafe.location,
        seats = cafe.seats,
        coffee_price = cafe.coffee_price,
    )
    form.submit.label.text = "Modify"

    if form.validate_on_submit():
        cafe.name = form.name.data
        cafe.map_url = form.map_url.data
        cafe.img_url = form.img_url.data
        cafe.location = form.location.data
        cafe.has_wifi = form.has_wifi.data
        cafe.has_toilet = form.has_toilet.data
        cafe.has_sockets = form.has_sockets.data
        cafe.can_take_calls = form.can_take_calls.data
        cafe.seats = form.seats.data
        cafe.coffee_price = form.coffee_price.data

        db.session.commit()

        return redirect(f"/cafes/{cafe.id}")
    


    return render_template('edit_cafe.html',cafe=cafe,form=form)

@app.route('/delete/<int:cafe_id>')
@confirmation_required
@login_required
def delete_cafe(cafe_id):
    cafe = db.get_or_404(Cafe,cafe_id)
    db.session.delete(cafe)
    db.session.commit()
    flash(f"{cafe.name} successfully deleted",'success')
    return redirect('/cafes')



@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')

    


if __name__=='__main__':
    app.run(debug=True)