import os
from flask import (
    Flask, flash, render_template, 
    redirect, request, session, url_for)
from flask_sqlalchemy import SQLAlchemy
from forms import UsersForm
from flask_login import LoginManager, login_required, current_user, login_user, logout_user, UserMixin


if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_DATABASE_URI")
db = SQLAlchemy(app)



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



@app.route('/admin')
@login_required
def admin():
    if current_user.is_authenticated:
        users_id = current_user.id
        users = User.query.all()
        return render_template('admin.html',users=users,users_id=users_id)
    else:
        username = current_user.username
        return render_template('no_booking.html', username=username)



if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)    