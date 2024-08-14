from flask import Flask,request, render_template, redirect, flash
from db import db, Cafe, User
from flask_bootstrap import Bootstrap5
from forms import RegisterUser, UserLogin
from flask_login import LoginManager, login_user
from werkzeug.security import generate_password_hash, check_password_hash
import os

from dotenv import load_dotenv; load_dotenv()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]=os.getenv("DATABASE_URI")
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

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
                password = generate_password_hash(form.password.data,method="scrypt:32768:8:1")
            )
            db.session.add(new_user)
            db.session.commit()
            flash("You have successfully registered","message")
            return redirect("/login")

    return render_template("register.html",form = form)

@app.route('/login',methods=["GET","POST"])
def login():
    form = UserLogin()
    
    if form.validate_on_submit():
        user = db.session.execute(db.select(User).where(User.email==form.email.data)).scalar()
        if user is not None and check_password_hash(user.password,form.password.data):
            login_user(user)
            flash("Successfully logged in")
            return redirect("/login")
        else:
            flash("Incorrect credentials")
            return redirect("/login")
        
    return render_template('login.html', form = form)


if __name__=='__main__':
    app.run(debug=True)