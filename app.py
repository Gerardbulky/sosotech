import os
from flask import (
    Flask, flash, render_template, 
    redirect, request, session, url_for)
from flask_sqlalchemy import SQLAlchemy
from forms import UsersForm, LoginForm, RegisterForm, ContactForm
from flask_login import LoginManager, login_required, current_user, login_user, logout_user, UserMixin
from datetime import datetime
from flask_bcrypt import Bcrypt
from flask_mail import Mail, Message
import smtplib

if os.path.exists("env.py"):
    import env


app = Flask(__name__)
mail = Mail(app) # instantiate the mail class

app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_DATABASE_URI")
db = SQLAlchemy(app) 
bcrypt = Bcrypt(app)
mail = Mail(app)

# initialize the app with the extension
db.init_app(app)

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
    phone = db.Column(db.String(150), unique= True)
    address = db.Column(db.String(150), unique= False)
    city_country = db.Column(db.String(150), unique= False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return '<User %r>' % self.fullname
    

with app.app_context():
    db.create_all()



@app.route("/", methods=["GET", "POST"])
def index():
    
    form = UsersForm()
    subject = 'Confirmation email!'
    if request.method == "POST" and form.validate_on_submit():
        email_already_exist = User.query.filter_by(email = form.email.data).first()
        phone_already_exist = User.query.filter_by(phone = form.phone.data).first()

        if email_already_exist or phone_already_exist:
            flash('Email or Phone number already exits')
            form = UsersForm()
            return redirect(url_for('.index'))    
        else:
            fullname = form.fullname.data 
            email = form.email.data 
            phone = form.phone.data 
            address = form.address.data 
            city_country = form.city_country.data
            users_info = User(fullname=fullname, email=email, phone=phone,address=address, city_country=city_country)
            db.session.add(users_info)
            db.session.commit()

    
        message = (f"From: {os.environ.get('MAIL_USERNAME')}\nTo: {email}\nSubject: {subject}\n\n"
                   f"Hello {form.fullname.data.split(' ')[0]}! \n\n  This email is to confirm that, your application has been received successfully. "
                        "Your information is as follows.  \n\n "
                        "Full names: {} \n Email: {} \n Phone: {} \n Address: {} \n City and Country: {} \n\n"
                        "If you have any questions, you can send us an email from the contact page. \n"
                        "Thanks for your application and for believing in us! "
                        "\n\n Best regards,  \n\n"
                        "SosoTechnology. ").format(form.fullname.data, form.email.data, form.phone.data, form.address.data, form.city_country.data) 
        # By encoding the message string to UTF-8, you can ensure that it supports a wide range of characters and prevent the "UnicodeEncodeError" from occurring
        message = message.encode('utf-8')
        server = smtplib.SMTP(os.environ.get("MAIL_SERVER"), os.environ.get("MAIL_PORT"))
        server.starttls()
        server.login(os.environ.get("MAIL_USERNAME"),os.environ.get("MAIL_PASSWORD"))
        server.sendmail(os.environ.get("MAIL_USERNAME"), email, message)
        
        session['name'] = form.fullname.data 
        email = '' 
        phone = ''
        address = ''
        city_country = ''
        flash(f"Thanks {session['name'].split(' ')[0]} for registering and email has been sent to you.", 'success')
        return redirect('/')
    return render_template("index.html", form=form)


@app.route('/contact/', methods=["GET", "POST"])
def contact():
    form = ContactForm()

    if request.method == "POST" and form.validate_on_submit():
        email = form.email.data
        subject = 'Confirmation Email'
        message = (f"From: {os.environ.get('MAIL_USERNAME')}\nTo: {email}\nSubject: {subject}\n\n"
                f"Hello {email.split('@')[0]}!\n\nThis is a confirmation email, that we have received your message. We will get back to you as soon as possible. \n"
                "Thanks for contacting us."
                "\n\n Best regards,  \n") 
        # Encode the message string to UTF-8 encoding format
        message = message.encode('utf-8')
        server = smtplib.SMTP(os.environ.get("MAIL_SERVER"), os.environ.get("MAIL_PORT"))
        server.starttls()
        server.login(os.environ.get("MAIL_USERNAME"),os.environ.get("MAIL_PASSWORD"))
        server.sendmail(os.environ.get("MAIL_USERNAME"), [email], message)
        
        session['name'] = form.name.data 
        email = '' 
        flash(f"Thanks {session['name'].split(' ')[0]} We have received your email.", 'success')
        return redirect('.')
    return render_template("contact.html", form=form)



@app.route('/register/', methods=['GET', 'POST'])
def register():
    email = None
    form = RegisterForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = Register.query.filter_by(email=form.email.data).first()  # We search the database if the email exits
        if email:
            flash('Email already exist')
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
    all_users = User.query.order_by(User.date_created).all()
    return render_template("profile.html", all_users=all_users, title="All Registered Users")


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)    