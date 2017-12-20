from . import admin, check_admin
from .. import db

from flask import render_template, flash, redirect, url_for
from flask_login import login_required

from .forms import ClassroomEditForm

from ..models import Classroom, RoomSpecialization


@admin.route('/classrooms/<int:pagin>')
@login_required
def list_classrooms(pagin):
    """
    Show classroom list
    """
    check_admin()

    classrooms = Classroom.query.order_by(Classroom.name).paginate(page=pagin, per_page=5)
    return render_template('admin/classrooms/classrooms.html',
                           classrooms=classrooms)


@admin.route('/classrooms/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_classroom(id):
    """
    Delete classroom
    """
    check_admin()

    try:
        classroom = Classroom.query.get_or_404(id)
        db.session.delete(classroom)
        db.session.commit()
        flash('You have successfully deleted the Classroom.', category='message')
    except:
        flash('Error in removing the Classroom.', category='error')

    # redirect to the list of classroom PAGE
    return redirect(url_for('admin.list_classrooms', pagin=1))


@admin.route('/classrooms/add', methods=['GET', 'POST'])
@login_required
def add_classroom():
    """
    Add classroom
    """
    check_admin()

    form = ClassroomEditForm()
    if form.validate_on_submit():
        try:
            classroom = Classroom(name=form.name.data,
                                  room_specialization_id=form.spec.data.id)
            db.session.add(classroom)
            db.session.commit()
            flash('You have successfully added a new Classroom.', category='message')
        except:
            flash('Error: Classroom Specialization name already exists.', category='error')

        # redirect to the list of classroom PAGE
        return redirect(url_for('admin.list_classrooms', pagin=1))

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
            flash('You have successfully changed name of the Classroom Specialization.', category='message')
        except:
            flash('Error in changing the name of the Classroom Specialization.', category='error')

        # redirect to the list of classroom PAGE
        return redirect(url_for('admin.list_classrooms', pagin=1))

    form.name.data = classroom.name
    form.spec.data = RoomSpecialization.query.get_or_404(classroom.room_specialization_id)

    return render_template('admin/classrooms/classroom.html',
                           classroom_name=classroom.name,
                           form=form,
                           title='Edit Classroom')