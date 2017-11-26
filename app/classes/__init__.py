from flask import Blueprint

classes = Blueprint('classes', __name__)

from . import views
