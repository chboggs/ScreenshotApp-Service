import os, sys, inspect, hashlib, re
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from flask import *
from models import User
from factory import db
from http_codes import *

new_user_blueprint = Blueprint('new_user_blueprint', __name__, template_folder='templates')

@new_user_blueprint.route('/new-user', methods=['POST', 'GET'])
def new_user():
    if request.method == 'GET':
        return render_template('new_user.html'), Status.HTTP_OK_BASIC
    else:
        username = request.form['username']
        password = request.form['password']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']

        if username == "" or password == "" or first_name == "" or last_name == "" or email == "":
            options = {
                "error": True,
                "problem": { "All fields must be filled out" }
            }
            return render_template("new_user.html", **options), Status.HTTP_BAD_REQUEST

        if re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email) == None:
            options = {
                "error": True,
                "problem": { "Must enter a valid email" }
            }
            return render_template("new_user.html", **options), Status.HTTP_BAD_REQUEST

        if not any(x.isupper() for x in password) or len(password) < 8 == None:
            options = {
                "error": True,
                "problem": { "Password must be eight characters and have an uppercase letter" }
            }
            return render_template("new_user.html", **options), Status.HTTP_BAD_REQUEST

        m = hashlib.new('sha512')
        m.update(password.encode('utf-8'))
        password = m.hexdigest()

        if User.query.filter(User.username == username).first():
            options = {
                "error": True,
                "problem": { "Account with specified username already exists" }
            }
            return render_template("new_user.html", **options), Status.HTTP_BAD_REQUEST

        if User.query.filter(User.email == email).first():
            options = {
                "error": True,
                "problem": { "Account with specified email already exists" }
            }
            return render_template("new_user.html", **options), Status.HTTP_BAD_REQUEST

        db.session.add(User(
            username=username, email=email, password=password, first_name=first_name, last_name=last_name
            ))
        db.session.commit()

        session['username'] = username
        return redirect(url_for('overview_blueprint.user_overview'))
