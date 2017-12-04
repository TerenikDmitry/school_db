from . import admin, check_admin
from .. import db

from flask import render_template, flash, redirect, url_for
from flask_login import login_required

from forms import StudentToClassEditForm

from ..models import User, StudentInClass, Class

@admin.route('/students_class')
@login_required
def list_students_class():
    """
    A list link between students and class
    """
    check_admin()

    students = User.query.filter_by(role_id=2).order_by(User.last_name).outerjoin(StudentInClass, User.id==StudentInClass.user_id_studen).all()

    return render_template('admin/students/list.html',
                           students=students)


@admin.route('/students_class/add/<int:id>', methods=['GET', 'POST'])
@login_required
def add_students_class(id):
    """
    Add link between students and class
    """
    check_admin()

    student = User.query.get_or_404(id)

    form = StudentToClassEditForm()
    if form.validate_on_submit():
        student_to_class = StudentInClass(class_id=form.class_name.data.id,
                                          user_id_studen=id)

        try:
            db.session.add(student_to_class)
            db.session.commit()
            flash('You have successfully added a new link between student and class.')
        except:
            flash('Error')

        # redirect to the list links between students and class PAGE
        return redirect(url_for('admin.list_students_class'))

    return render_template('admin/students/edit.html',
                           form=form,
                           student=student,
                           title='Add link between student and class')


@admin.route('/students_class/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_students_class(id):
    """
    Delete link between students and class
    """
    check_admin()

    student_to_class = StudentInClass.query.filter_by(user_id_studen=id).first()
    db.session.delete(student_to_class)
    db.session.commit()
    flash('You have successfully deleted link between students and class.')

    # redirect to the list links between parents and students PAGE
    return redirect(url_for('admin.list_students_class'))


@admin.route('/students_class/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_students_class(id):
    """
    Edit link between students and class
    """
    check_admin()

    student = User.query.get_or_404(id)
    student_to_class = StudentInClass.query.filter_by(user_id_studen=id).first()

    form = StudentToClassEditForm()
    if form.validate_on_submit():
        if student_to_class:
            student_to_class.class_id = form.class_name.data.id
        else:
            student_to_class = StudentInClass(user_id_studen=id,
                                              class_id=form.class_name.data.id)

        try:
            db.session.add(student_to_class)
            db.session.commit()
            flash('You have successfully added a new classroom.')
        except:
            flash('Error')

        # redirect to the list links between students and class PAGE
        return redirect(url_for('admin.list_students_class'))

    form.class_name.query = db.session.query(Class)
    if student_to_class:
        form.class_name.data = Class.query.get(student_to_class.class_id)
    return render_template('admin/students/edit.html',
                           form=form,
                           student=student,
                           title='Edit link between student and class')