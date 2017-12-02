from . import admin, check_admin
from .. import db

from flask import render_template, flash, redirect, url_for
from flask_login import login_required

from forms import ClassroomEditForm

from ..models import Classroom, RoomSpecialization


@admin.route('/classrooms')
@login_required
def list_classrooms():
    """
    Show classroom list
    """
    check_admin()

    classrooms = Classroom.query.all()
    return render_template('admin/classrooms/classrooms.html',
                           classrooms=classrooms)


@admin.route('/classrooms/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_classroom(id):
    """
    Delete classroom
    """
    check_admin()

    classroom = Classroom.query.get_or_404(id)
    db.session.delete(classroom)
    db.session.commit()
    flash('You have successfully deleted the classroom specialization.')

    # redirect to the list of classroom PAGE
    return redirect(url_for('admin.list_room_specializations'))


@admin.route('/classrooms/add', methods=['GET', 'POST'])
@login_required
def add_classroom():
    """
    Add classroom
    """
    check_admin()

    form = ClassroomEditForm()
    if form.validate_on_submit():
        classroom = Classroom(name=form.name.data,
                              room_specialization_id=form.spec.data.id)

        try:
            db.session.add(classroom)
            db.session.commit()
            flash('You have successfully added a new classroom.')
        except:
            flash('Error: classroom name already exists.')

        # redirect to the list of classroom PAGE
        return redirect(url_for('admin.list_classrooms'))

    return render_template('admin/classrooms/classroom.html',
                           form=form,
                           title='Add Classroom')


@admin.route('/classrooms/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_classroom(id):
    """
    Edit classroom
    """
    check_admin()

    classroom = Classroom.query.get_or_404(id)

    form = ClassroomEditForm()
    if form.validate_on_submit():
        try:
            classroom.name = form.name.data
            classroom.room_specialization_id = form.spec.data.id
            db.session.add(classroom)
            db.session.commit()
            flash('You have successfully added a new classroom.')
        except:
            flash('Error: classroom name already exists.')

        # redirect to the list of classroom PAGE
        return redirect(url_for('admin.list_classrooms'))

    form.name.data = classroom.name
    form.spec.data = RoomSpecialization.query.get_or_404(classroom.room_specialization_id)

    return render_template('admin/classrooms/classroom.html',
                           form=form,
                           title='Edit Classroom')