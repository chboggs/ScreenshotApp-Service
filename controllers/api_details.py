import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from flask import *
from models import User, Image, Comments, Viewable
from factory import db
from http_codes import *

api_details_blueprint = Blueprint('api_details_blueprint', __name__, template_folder='templates')

@api_details_blueprint.route('/api/add_viewer', methods=['POST'])
def add_viewer_api():
    print("Got to add viewer")
    image_id = request.form['image_id']
    new_viewer = request.form['new_viewer']
    print("image_id: " + str(image_id))
    print("new_viewer: " + str(new_viewer))

    if not image_id or not new_viewer:
        print("first")
        return "Missing required parameter", Status.HTTP_BAD_REQUEST

    if not User.query.filter(User.username == new_viewer).first() or not Image.query.filter(Image.id == image_id).first():
        print("second")
        return "Invalid user or filename", Status.HTTP_BAD_REQUEST

    print("third")
    owner = User.query.filter(User.username == Image.query.filter(Image.id == image_id).first().owner).first()
    current_user = session['username']
    if current_user != owner.username:
        print("fourth")
        return "You do not own this image", Status.HTTP_BAD_FORBIDDEN

    image = Image.query.filter(Image.id == image_id).first()

    print("fifth")
    if new_viewer == owner.username:
        print("sixth")
        return "User " + new_viewer + " owns this image", Status.HTTP_BAD_REQUEST
    if Viewable.query.filter(Viewable.image_name == image.name and Viewable.user_name == new_viewer).first():
        print("seventh")
        return "User " + new_viewer + " can already view this image", Status.HTTP_BAD_REQUEST

    print("eighth")
    db.session.add(Viewable(
        image_name=image.name, image_id=image_id, user_name=new_viewer
        ))
    db.session.commit()
    print("ninth")

    return "Successfully granted permission to " + new_viewer, Status.HTTP_OK_BASIC

@api_details_blueprint.route('/api/add_comment', methods=['POST'])
def add_comment_api():
    query_params = dict(request.args)

    if 'image_id' not in query_params or 'new_viewer' not in query_params:
        return "Missing required parameter", Status.HTTP_BAD_REQUEST

    image_id = query_params['image_id'][0]
    new_viewer = query_params['new_viewer'][0]

    if not User.query.filter(User.username == new_viewer).first() or not Image.query.filter(Image.id == image_id).first():
        return "Invalid user or filename", Status.HTTP_BAD_REQUEST

    owner = User.query.filter(User.username == Image.query.filter(Image.id == image_id).first().owner).first()
    current_user = session['username']
    if current_user != owner.username:
        return "You do not own this image", Status.HTTP_BAD_FORBIDDEN

    image = Image.query.filter(Image.id == image_id).first()

    if new_viewer == owner.username:
        return "User " + new_viewer + " owns this image", Status.HTTP_BAD_REQUEST
    if Viewable.query.filter(Viewable.image_name == image.name and Viewable.user_name == new_viewer).first():
        return "User " + new_viewer + " can already view this image", Status.HTTP_BAD_REQUEST

    db.session.add(Viewable(
        image_name=image.name, image_id=image_id, user_name=new_viewer
        ))
    db.session.commit()

    return "Successfully granted permission to " + new_viewer, Status.HTTP_OK_BASIC
