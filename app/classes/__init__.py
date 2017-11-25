from flask import Blueprint

class_room = Blueprint('class_room', __name__)

from . import views
