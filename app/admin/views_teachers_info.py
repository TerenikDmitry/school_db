from flask import flash, redirect, render_template, url_for
from flask_login import login_required

from . import admin, check_admin
from .. import db
from .forms import TeacherSubjectAddForm, TeacherClassroomEditForm
from ..models import User, TeacherToSubject, TeachersClassroom, Classroom, Subject


@admin.route('/teachers/list/<int:pagin>')
@login_required
def list_teachers_info(pagin):
    """
    A list with info about teachers
    """
    check_admin()

    teachers = User.query.filter_by(role_id=1).order_by(User.last_name).paginate(page=pagin, per_page=10)

    return render_template('admin/teachers/list.html',
                           teachers=teachers)


@admin.route('/teachers/<int:id_teacher>/subject/add', methods=['GET', 'POST'])
@login_required
def add_teacher_subjects(id_teacher):
    """
    Add subject to the list of teacher subjects
    """
    check_admin()

    teacher = User.query.get_or_404(id_teacher)

    form = TeacherSubjectAddForm()
    if form.validate_on_submit():
        try:
            subject = Subject.query.get_or_404(form.subject.data.id)
            teacher_subject = TeacherToSubject(user_id_teacher=id_teacher,
                                               subject_id=subject.id)
            db.session.add(teacher_subject)
            db.session.commit()
            flash('You have successfully added a subject to the list of teacher\'s subjects.', category='message')
        except:
            flash('Error in adding an item to the list of teacher\'s subjects. This relationship already exists.', category='error')

        # redirect to the list links between students and class PAGE
        return redirect(url_for('admin.edit_teacher_subjects', id_teacher=id_teacher))

    return render_template('admin/teachers/subject_add.html',
                           form=form,
                           teacher=teacher)


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

    try:
        teacher_subject = TeacherToSubject.query.filter(TeacherToSubject.subject_id == id_subject,
                                                         TeacherToSubject.user_id_teacher == id_teacher).first()
        db.session.delete(teacher_subject)
        db.session.commit()
        flash('You successfully deleted an item from the teacher\'s subject list.', category='message')
    except:
        flash('Error in removing the item from the teacher\'s subject list', category='error')

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
        try:
            classroom = Classroom.query.get_or_404(form.classroom.data.id)
            teacher_classroom = TeachersClassroom(user_id_teacher=id_teacher,
                                                  classroom_id=classroom.id)
            db.session.add(teacher_classroom)
            db.session.commit()
            flash('You have successfully added a link between Teacher and the Classroom.', category='message')
        except:
            flash('Error in linking between Teacher and Class', category='error')

        # redirect to the list of Teachers
        return redirect(url_for('admin.list_teachers_info', pagin=1))

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
        try:
            classroom = Classroom.query.get_or_404(form.classroom.data.id)
            teacher_classroom.classroom_id = classroom.id
            db.session.add(teacher_classroom)
            db.session.commit()
            flash('You have successfully changed a link between Teacher and the Classroom.', category='message')
        except:
            flash('Error in changing the binding between Teacher and Class', category='error')

        # redirect to the list of Teachers
        return redirect(url_for('admin.list_teachers_info', pagin=1))

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
    try:
        teacher_classroom = TeachersClassroom.query.filter(TeacherToSubject.user_id_teacher == id_teacher).first()
        db.session.delete(teacher_classroom)
        db.session.commit()
        flash('You have successfully deleted link between Teacher and Classroom.')
    except:
        flash('An error in deleting the relationship between Teacher and Classroom', category='error')

    return redirect(url_for('admin.list_teachers_info', pagin=1))