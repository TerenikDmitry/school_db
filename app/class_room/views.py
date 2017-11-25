from flask import abort, flash, redirect, render_template, url_for

from flask_login import current_user, login_required
from . import class_room
from ..models import Class, StudentInClass

@class_room.route('/class/<int:class_id>')
@login_required
def classRoom(class_id):
    classStudents = StudentInClass.query.filter_by(class_id=class_id).all()
    _class = Class.query.get_or_404(class_id)

    return render_template('class_room/class.html', title='Class', _class=_class, classStudents=classStudents)