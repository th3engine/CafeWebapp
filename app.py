from flask import Flask,request, render_template
from db import db, Cafe
from flask_bootstrap import Bootstrap5
from forms import RegisterUser
import os

from dotenv import load_dotenv; load_dotenv()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]=os.getenv("DATABASE_URI")
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

Bootstrap5(app)

db.init_app(app)
with app.app_context():
    db.create_all()

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
        pass

    return render_template("register.html",form = form)





if __name__=='__main__':
    app.run(debug=True)