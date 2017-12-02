from . import admin, check_admin
from .. import db

from flask import render_template, flash, redirect, url_for
from flask_login import login_required

from forms import ParentToStudentAddForm, ParentToStudentEditForm

from ..models import User, ParentToStudent


@admin.route('/parent_to_student')
@login_required
def list_parent_to_student():
    """
    A list link between parents and students
    """
    check_admin()

    parent_to_student = ParentToStudent.query.all()

    return render_template('admin/parent_to_student/list.html',
                           parent_to_student=parent_to_student)


@admin.route('/parent_to_student/add', methods=['GET', 'POST'])
@login_required
def add_parent_to_student():
    """
    Add link between parents and students
    """
    check_admin()

    add_parent_to_student = True

    form = ParentToStudentAddForm()
    if form.validate_on_submit():
        parent_to_student = ParentToStudent(user_id_parent=form.parent.data.id,
                                    user_id_student=form.student.data.id)

        try:
            db.session.add(parent_to_student)
            db.session.commit()
            flash('You have successfully added a new link between parents and students.')
        except:
            flash('Error')

        # redirect to the list links between parents and students PAGE
        return redirect(url_for('admin.list_parent_to_student'))

    form.parent.query = db.session.query(User).filter(User.role_id == 3)
    form.student.query = db.session.query(User).filter(User.role_id == 2)
    return render_template('admin/parent_to_student/edit.html',
                           form=form,
                           add_parent_to_student=add_parent_to_student,
                           title='Add link between parents and students')


@admin.route('/parent_to_student/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_parent_to_student(id):
    """
    Delete link between parents and students
    """
    check_admin()

    parent_to_student = ParentToStudent.query.get_or_404(id)
    db.session.delete(parent_to_student)
    db.session.commit()
    flash('You have successfully deleted link between parents and students.')

    # redirect to the list links between parents and students PAGE
    return redirect(url_for('admin.list_parent_to_student'))


@admin.route('/parent_to_student/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_parent_to_student(id):
    """
    Edit link between parents and students
    """
    check_admin()

    add_parent_to_student = False

    parent_to_student = ParentToStudent.query.filter_by(user_id_parent=id).first()
    parent_name = '{}'.format(parent_to_student.parentStudent)

    form = ParentToStudentEditForm()
    if form.validate_on_submit():
        parent_to_student.user_id_student = form.student.data.id

        try:
            db.session.add(parent_to_student)
            db.session.commit()
            flash('You have successfully added a new classroom.')
        except:
            flash('Error')

        # redirect to the list links between parents and students PAGE
        return redirect(url_for('admin.list_parent_to_student'))

    form.student.query = db.session.query(User).filter(User.role_id == 2)
    return render_template('admin/parent_to_student/edit.html',
                           form=form,
                           parent_name = parent_name,
                           add_parent_to_student=add_parent_to_student,
                           title='Edit link between parents and students')