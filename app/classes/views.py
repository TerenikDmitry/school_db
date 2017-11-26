from flask import abort, flash, redirect, render_template, url_for

from flask_login import current_user, login_required
from . import classes
from .. import db
from ..models import Class, StudentInClass, User, Classroom, Specialization
from forms import ClassForm, ClassStudentsForm


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
    List of classes
    """
    check_admin()

    classesList = Class.query.all()
    return render_template('classes/classes.html',
                           classesList=classesList)


@classes.route('/class/add', methods=['GET', 'POST'])
@login_required
def add_class():
    """
    Add class
    """
    check_admin()

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
            db.session.add(classOne)
            db.session.commit()
            flash('You have successfully added a new class.')
        except:
            flash('Error')

        # redirect to the list of classes PAGE
        return redirect(url_for('classes.list_classes'))

    return render_template('classes/editClass.html',
                           form=form,
                           title='Add Class')


@classes.route('/class/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_class(id):
    """
    Edit class
    """
    check_admin()

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
            flash('Error')

        # redirect to the list of classes PAGE
        return redirect(url_for('classes.list_classes'))

    form.name.data = classOne.name
    form.date_start.data = classOne.dateStartEducation
    form.date_end.data = classOne.dateEndEducation
    form.head_teacher_id.data = User.query.get_or_404(classOne.headTeacher)
    form.classroom_id.data = Classroom.query.get_or_404(classOne.room_id)
    form.specialization_id.data = Specialization.query.get_or_404(classOne.specialization_id)
    return render_template('classes/editClass.html',
                           form=form,
                           title="Edit Class")


@classes.route('/class/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_class(id):
    """
    Delete class
    """
    check_admin()

    classOne = Class.query.get_or_404(id)
    db.session.delete(classOne)
    db.session.commit()
    flash('You have successfully deleted the class.')

    # redirect to the list of classes PAGE
    return redirect(url_for('classes.list_classes'))


@classes.route('/class/students/add/<int:id>', methods=['GET', 'POST'])
@login_required
def add_student(id):
    """
    Add a student to class
    """
    check_admin()

    form = ClassStudentsForm(obj=id)
    if form.validate_on_submit():
        try:
            studentInClass = StudentInClass(class_id=id,
                                            user_id_studen=form.student.data.id)
            db.session.add(studentInClass)
            db.session.commit()
            flash('You have successfully added a student to class.')
        except:
            flash('Error')

        # redirect to the list of classes PAGE
        return redirect(url_for('classes.list_classes'))

    form.student.query = db.session.query(User).filter(User.role_id == 2).outerjoin(StudentInClass).filter(StudentInClass.user_id_studen == None)
    class_name = Class.query.get_or_404(id)
    return render_template('classes/addStudentToClass.html',
                           form=form,
                           class_name = class_name.name,
                           title='Add Student to Class')
