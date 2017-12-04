from flask import flash, redirect, render_template, url_for
from flask_login import login_required

from . import admin, check_admin
from .. import db
from forms import TeacherSubjectAddForm, TeacherClassroomEditForm
from ..models import User, TeacherToSubject, TeachersClassroom, Classroom, Subject


@admin.route('/teachers/list')
@login_required
def list_teachers_info():
    """
    A list with info about teachers
    """
    check_admin()

    teachers = User.query.filter_by(role_id=1).order_by(User.last_name).all()

    return render_template('admin/teachers/list.html',
                           teachers=teachers)


@admin.route('/teachers/<int:id_teacher>/subject/add', methods=['GET', 'POST'])
@login_required
def add_teacher_subjects(id_teacher):
    """
    Add subject to the list of teacher subjects
    """
    check_admin()

    form = TeacherSubjectAddForm()
    teacher = User.query.get_or_404(id_teacher)

    if form.validate_on_submit():
        subject = Subject.query.get_or_404(form.subject.data.id)
        teacher_subject = TeacherToSubject(user_id_teacher=id_teacher,
                                           subject_id=subject.id)

        try:
            db.session.add(teacher_subject)
            db.session.commit()
            flash('You have successfully added a subject to the list of teacher subjects.')
        except:
            flash('Error')

        # redirect to the list links between students and class PAGE
        return redirect(url_for('admin.edit_teacher_subjects', id_teacher=id_teacher))

    return render_template('admin/teachers/subject_add.html',form=form, teacher=teacher)


@admin.route('/teachers/<int:id_teacher>/subjects/edit/', methods=['GET', 'POST'])
@login_required
def edit_teacher_subjects(id_teacher):
    """
    Edit list of teacher subjects
    """
    check_admin()

    teacher = User.query.get_or_404(id_teacher)

    return render_template('admin/teachers/subjects.html', teacher=teacher)


@admin.route('/teachers/<int:id_teacher>/subject/delete/<int:id_subject>', methods=['GET', 'POST'])
@login_required
def delete_teacher_subjects(id_teacher, id_subject):
    """
    Delete a subject from list of teacher subjects
    """
    check_admin()

    teacher_subject = TeacherToSubject.query.filter(TeacherToSubject.subject_id == id_subject,
                                                     TeacherToSubject.user_id_teacher == id_teacher).first()
    db.session.delete(teacher_subject)
    db.session.commit()
    flash('You have successfully deleted link between students and class.')

    # redirect to the list links between parents and students PAGE
    return redirect(url_for('admin.edit_teacher_subjects', id_teacher=id_teacher))


@admin.route('/teachers/<int:id_teacher>/classroom/add', methods=['GET', 'POST'])
@login_required
def add_teacher_classroom(id_teacher):
    """
    Add teacher-classroom relationship
    """
    check_admin()

    teacher = User.query.get_or_404(id_teacher)
    add_classroom_link = True

    form = TeacherClassroomEditForm()
    if form.validate_on_submit():
        classroom = Classroom.query.get_or_404(form.classroom.data.id)
        teacher_classroom = TeachersClassroom(user_id_teacher=id_teacher,
                                              classroom_id=classroom.id)

        try:
            db.session.add(teacher_classroom)
            db.session.commit()
            flash('You have successfully added a link between Teacher and the Classroom.')
        except:
            flash('Error')

        # redirect to the list of Teachers
        return redirect(url_for('admin.list_teachers_info'))

    return render_template('admin/teachers/classroom_edit.html',
                           form=form,
                           add_classroom_link=add_classroom_link,
                           teacher=teacher)


@admin.route('/teachers/<int:id_teacher>/classroom/edit', methods=['GET', 'POST'])
@login_required
def edit_teacher_classroom(id_teacher):
    """
    Change teacher-classroom relationship
    """
    check_admin()

    teacher_classroom = TeachersClassroom.query.filter_by(user_id_teacher=id_teacher).first()

    form = TeacherClassroomEditForm()
    if form.validate_on_submit():
        classroom = Classroom.query.get_or_404(form.classroom.data.id)
        teacher_classroom.classroom_id = classroom.id

        try:
            db.session.add(teacher_classroom)
            db.session.commit()
            flash('You have successfully changed a link between Teacher and the Classroom.')
        except:
            flash('Error')

        # redirect to the list of Teachers
        return redirect(url_for('admin.list_teachers_info'))

    form.classroom.data = Classroom.query.get_or_404(teacher_classroom.classroom_id)

    return render_template('admin/teachers/classroom_edit.html',
                           form=form,
                           teacher=teacher_classroom.users)


@admin.route('/teachers/<int:id_teacher>/classroom/delete', methods=['GET', 'POST'])
@login_required
def delete_teacher_classroom(id_teacher):
    """
    Unbind teacher-classroom relationship
    """
    check_admin()

    teacher_classroom = TeachersClassroom.query.filter(TeacherToSubject.user_id_teacher == id_teacher).first()
    db.session.delete(teacher_classroom)
    db.session.commit()
    flash('You have successfully deleted link between teacher and classroom.')

    return redirect(url_for('admin.list_teachers_info'))