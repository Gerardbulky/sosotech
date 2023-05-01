import os
from flask import (
    Flask, flash, render_template, 
    redirect, request, session, url_for)
from flask_sqlalchemy import SQLAlchemy
from forms import UsersForm, LoginForm, RegisterForm
from flask_login import LoginManager, login_required, current_user, login_user, logout_user, UserMixin
from datetime import datetime
from flask_bcrypt import Bcrypt

if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_DATABASE_URI")
db = SQLAlchemy(app) 
bcrypt = Bcrypt(app)

class Register(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    email = db.Column(db.String(50), unique= True, nullable=False)
    password = db.Column(db.String(200), unique= False, nullable=False)
    confirm = db.Column(db.String(200), unique= False, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return '<Register %r>' % self.email

with app.app_context():
    db.create_all()


class Login(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    email = db.Column(db.String(50), unique= True, nullable=False)
    password = db.Column(db.String(200), unique= False, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return '<Login %r>' % self.email

with app.app_context():
    db.create_all()
    

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(150), unique=False, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    phone = db.Column(db.String(150), unique= False)
    city_country = db.Column(db.String(150), unique= False)

    def __repr__(self):
        return '<User %r>' % self.fullname
    

with app.app_context():
    db.create_all()



@app.route("/", methods=["GET", "POST"])
def index():
    form = UsersForm()
    if request.method == "POST":
        fullname = form.fullname.data 
        email = form.email.data 
        phone = form.phone.data 
        city_country = form.city_country.data 

        users_info = User(fullname=fullname, email=email, phone=phone, city_country=city_country)
        db.session.add(users_info)
        db.session.commit()
        flash("Thanks for registering and email has been sent to you.", 'success')
        return redirect('/')
    return render_template("index.html", form=form)



@app.route('/register/', methods=['GET', 'POST'])
def register():
    email = None
    form = RegisterForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = Register.query.filter_by(email=form.email.data).first()
        if not email:
            form = RegisterForm()
        else:
            hash_password = bcrypt.generate_password_hash(form.password.data)
            register_user = Register(email=form.email.data, password=hash_password)
            db.session.add(register_user)
            db.session.commit()
        # Extrating username from email
        extract_email = form.email.data.index("@")[0]
        result = ""
        for i in extract_email:
            if i.isalpha():
                result+=i
        session["user"]= result
        form.password.data = ''

        flash(f'Welcome {session["result"]} Thank you for registering!', 'success')
        return redirect(url_for("register"))
    flash("Email already exist", "danger")
    return render_template("register.html", form=form, title="Registration Page")



@app.route('/login/', methods=["GET", "POST"])
def login():
	form = LoginForm()
	if request.method == "POST" and form.validate_on_submit():
		email = Register.query.filter_by(email=form.email.data).first()
        
		if email and bcrypt.check_password_hash(email.password, form.password.data):
			login_user(email)
			flash(f"Hello {form.email.data.capitalize()}, You are login now!", "success")
			next = request.args.get('next')
			return redirect(next or url_for(".index"))
		flash('Incorrect email or password', "danger")
		return redirect(url_for('login'))
	return render_template("login.html", form=form, title="Login Page")



if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)    