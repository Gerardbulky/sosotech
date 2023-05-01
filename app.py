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


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view='login'
login_manager.needs_refresh_message_category='danger'
login_manager.login_message = u"Please login first"



@login_manager.user_loader
def user_loader(user_id):
	return Register.query.get(user_id)

class Register(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key= True)
    email = db.Column(db.String(50), unique= True, nullable=False)
    password = db.Column(db.String(200), unique= True, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return '<Register %r>' % self.email

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
        email = Register.query.filter_by(email=form.email.data).first()  # We search the database if the email exits
        if email:
            form = RegisterForm()
        else:
            hash_password = bcrypt.generate_password_hash(form.password.data)
            register_user = Register(email=form.email.data, password=hash_password)
            db.session.add(register_user)
            db.session.commit()
        # # Extrating username from email
        extract_username_from_email = form.email.data.strip()
        extracted_username = extract_username_from_email[:extract_username_from_email.index('@')]
        
        session["user"]= extracted_username
        form.email.data = ''
        form.password.data = ''

        flash(f'Welcome {session["user"]} Thank you for registering!', 'success')
        return redirect(url_for("login"))
    return render_template("register.html", form=form, title="Registration Page")


@app.route('/login/', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == "POST" and form.validate_on_submit():
        user = Register.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data): 
            login_user(user)
            flash(f"Hello {form.email.data.capitalize()}, You are login now!", "success")
            next = request.args.get('next')
            return redirect(next or url_for(".profile"))
        flash('Incorrect email or password', "danger")
        return redirect(url_for('login'))
    return render_template("login.html", form=form, title="Login Page")


@app.route('/logout/')
def logout():
    logout_user()
    flash('You are now sign out', "danger")
    return redirect(url_for('.index'))


@app.route('/profile/', methods=["GET", "POST"])
@login_required
def profile():
	return render_template("profile.html", title="profile Page")



if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)    