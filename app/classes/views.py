from flask import abort, flash, redirect, render_template, url_for

from flask_login import current_user, login_required
from . import classes
from .. import db
from ..models import Class, StudentInClass, User, Classroom, Specialization
from forms import ClassForm


def check_admin():
    """
    Prevent non-admins from accessing the page
    """
    if not current_user.is_admin:
        abort(403)


@classes.route('/class/<int:class_id>')
@login_required
def one_class(class_id):
    classStudents = StudentInClass.query.filter_by(class_id=class_id).all()
    _class = Class.query.get_or_404(class_id)

    return render_template('classes/class.html', title='Class', _class=_class, classStudents=classStudents)


@classes.route('/class/list')
@login_required
def list_classes():
    """
        List of classes from the database
    """
    check_admin()

    classesList = Class.query.all()
    return render_template('classes/classes.html', classesList=classesList, title='Classes')


@classes.route('/class/add', methods=['GET', 'POST'])
@login_required
def add_class():
    """
        Add a class to the database
    """
    check_admin()

    add_class = True

    form = ClassForm()
    if form.validate_on_submit():
        try:
            classOne = Class(name=form.name.data,
                             dateStartEducation=form.date_start.data,
                             dateEndEducation=form.date_end.data,
                             headTeacher=form.head_teacher_id.data.id,
                             room_id=form.classroom_id.data.id,
                             specialization_id=form.specialization_id.data.id
                             )
            # add role to the database
            db.session.add(classOne)
            db.session.commit()
            flash('You have successfully added a new class.')
        except:
            # in case role name already exists
            flash('Error')

        # redirect to the roles page
        return redirect(url_for('classes.list_classes'))

    # load role template
    return render_template('classes/editClass.html', add_class=add_class,
                           form=form, title='Add Class')


@classes.route('/class/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_class(id):
    """
    Edit a role
    """
    check_admin()

    add_class = False

    classOne = Class.query.get_or_404(id)
    form = ClassForm(obj=classOne)
    if form.validate_on_submit():
        classOne.name = form.name.data
        classOne.dateStartEducation = form.date_start.data
        classOne.dateStartEducation = form.date_end.data
        classOne.headTeacher = form.head_teacher_id.data.id
        classOne.room_id = form.classroom_id.data.id
        classOne.specialization_id = form.specialization_id.data.id

        try:
            db.session.add(classOne)
            db.session.commit()
            flash('You have successfully edited the class.')
        except:
            # in case role name already exists
            flash('Error')

        # redirect to the roles page
        return redirect(url_for('classes.list_classes'))

    form.name.data = classOne.name
    form.date_start.data = classOne.dateStartEducation
    form.date_end.data = classOne.dateEndEducation
    form.head_teacher_id.data = User.query.get_or_404(classOne.headTeacher)
    form.classroom_id.data = Classroom.query.get_or_404(classOne.room_id)
    form.specialization_id.data = Specialization.query.get_or_404(classOne.specialization_id)
    return render_template('classes/editClass.html', add_class=add_class,
                           form=form, title="Edit Class")


@classes.route('/class/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_class(id):
    """
    Delete a role from the database
    """
    check_admin()

    classOne = Class.query.get_or_404(id)
    db.session.delete(classOne)
    db.session.commit()
    flash('You have successfully deleted the class.')

    # redirect to the roles page
    return redirect(url_for('classes.list_classes'))