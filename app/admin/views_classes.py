from flask import abort, flash, redirect, render_template, url_for

from flask_login import current_user, login_required
from . import admin
from .. import db
from ..models import Class, StudentInClass, User, Classroom, Specialization
from .forms import ClassForm, ClassStudentsForm


def check_admin():
    """
    Prevent non-admins from accessing the page
    """
    if not current_user.is_admin:
        abort(403)


@admin.route('/class/list/<int:pagin>')
@login_required
def list_classes(pagin):
    """
    List of classes
    """
    check_admin()

    classesList = Class.query.order_by(Class.name).paginate(page=pagin, per_page=5)
    return render_template('admin/classes/class.html',
                           classesList=classesList)


@admin.route('/class/add', methods=['GET', 'POST'])
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
                             dateStartEducation=form.dateStartEducation.data,
                             dateEndEducation=form.dateEndEducation.data,
                             headTeacher=form.headTeacher.data.id,
                             room_id=form.room_id.data.id,
                             specialization_id=form.specialization_id.data.id
                             )
            db.session.add(classOne)
            db.session.commit()
            flash('You have successfully added a new class.',category='message')
        except:
            flash('Add the class error.',category='error')

        # redirect to the list of classes PAGE
        return redirect(url_for('classes.list_classes', pagin=1))

    form.headTeacher.query = User.query.filter(User.is_admin!=True, User.role_id==1).outerjoin(Class, Class.headTeacher == User.id).filter(Class.id==None)

    return render_template('admin/classes/editClass.html',
                           form=form,
                           title='Add Class')


@admin.route('/class/<int:id>/edit', methods=['GET', 'POST'])
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
        classOne.dateStartEducation = form.dateStartEducation.data
        classOne.dateEndEducation = form.dateEndEducation.data
        classOne.headTeacher = form.headTeacher.data.id
        classOne.room_id = form.room_id.data.id
        classOne.specialization_id = form.specialization_id.data.id

        try:
            db.session.add(classOne)
            db.session.commit()
            flash('You have successfully edited the class.',category='message')
        except:
            flash('Edited the class error',category='error')

        # redirect to the list of classes PAGE
        return redirect(url_for('admin.list_classes', pagin=1))

    form.headTeacher.data = User.query.get_or_404(classOne.headTeacher)
    form.room_id.data = Classroom.query.get_or_404(classOne.room_id)
    form.specialization_id.data = Specialization.query.get_or_404(classOne.specialization_id)
    return render_template('admin/classes/editClass.html',
                           form=form,
                           class_name=classOne.name,
                           title="Edit Class")


@admin.route('/class/<int:id>/delete', methods=['GET', 'POST'])
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
    return redirect(url_for('admin.list_classes', pagin=1))


@admin.route('/class/<int:id>/students/add', methods=['GET', 'POST'])
@login_required
def add_student(id):
    """
    Add class
    """
    check_admin()

    form = ClassStudentsForm()
    if form.validate_on_submit():
        try:
            classStudent = StudentInClass(class_id=id,
                                          user_id_studen=form.student.data.id)
            db.session.add(classStudent)
            db.session.commit()
            flash('You have successfully added a student to the class.',category='message')
        except:
            flash('Error in adding student to class',category='error')

        # redirect to the list of classes PAGE
        return redirect(url_for('admin.list_classes', pagin=1))

    form.student.query = User.query.filter_by(role_id=2).outerjoin(StudentInClass, StudentInClass.user_id_studen == User.id).filter(StudentInClass.class_id==None)

    return render_template('admin/classes/editStudentToClass.html',
                           form=form,
                           title='Add Student')


@admin.route('/class/<int:id>/students/edit', methods=['GET', 'POST'])
@login_required
def list_students(id):
    """
    Add a student to class
    """
    check_admin()

    students = StudentInClass.query.filter_by(class_id=id).all()
    oneClass = Class.query.get_or_404(id)

    return render_template('admin/classes/listStudentToClass.html',
                           students=students,
                           oneClass=oneClass,
                           title='Add Student to Class')


@admin.route('/class/<int:id_class>/students/delete/<int:id_student>', methods=['GET', 'POST'])
@login_required
def delete_student(id_class,id_student):
    """
    Delete a Student from Class
    """
    check_admin()

    try:
        students = StudentInClass.query.filter(StudentInClass.class_id == id_class,
                                               StudentInClass.user_id_studen == id_student).first()
        db.session.delete(students)
        db.session.commit()
        flash('You have successfully deleted student from class.',category='message')
    except:
        flash('Error in removing student from class', category='error')

    # redirect to the list of classes PAGE
    return redirect(url_for('admin.list_classes', pagin=1))