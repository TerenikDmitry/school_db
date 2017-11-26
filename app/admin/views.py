from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from . import admin
from .. import db
from forms import *
from ..models import Role, User, Specialization, RoomSpecialization, Classroom, ParentToStudent, StudentInClass


def check_admin():
    """
    Prevent non-admins from accessing the page
    """
    if not current_user.is_admin:
        abort(403)


@admin.route('/roles')
@login_required
def list_roles():
    """
    Show roles
    """
    check_admin()

    roles = Role.query.all()

    return render_template('admin/roles/roles.html',
                           roles=roles,
                           title='Roles')


@admin.route('/roles/add', methods=['GET', 'POST'])
@login_required
def add_role():
    """
    Add a role
    """
    check_admin()

    form = RoleForm()
    if form.validate_on_submit():
        role = Role(name=form.name.data,
                    description=form.description.data)

        try:
            # add role to the database
            db.session.add(role)
            db.session.commit()
            flash('You have successfully added a new role.')
        except:
            flash('Error: role name already exists.')

        # redirect to the list roles PAGE
        return redirect(url_for('admin.list_roles'))

    return render_template('admin/roles/role.html',
                           form=form,
                           title='Add Role')


@admin.route('/roles/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_role(id):
    """
    Edit a role
    """
    check_admin()

    role = Role.query.get_or_404(id)
    form = RoleForm(obj=role)
    if form.validate_on_submit():
        role.name = form.name.data
        role.description = form.description.data
        db.session.add(role)
        db.session.commit()
        flash('You have successfully edited the role.')

        # redirect to the list roles PAGE
        return redirect(url_for('admin.list_roles'))

    form.description.data = role.description
    form.name.data = role.name

    return render_template('admin/roles/role.html',
                           form=form,
                           title="Edit Role")


@admin.route('/roles/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_role(id):
    """
    Delete a role
    """
    check_admin()

    role = Role.query.get_or_404(id)
    db.session.delete(role)
    db.session.commit()
    flash('You have successfully deleted the role.')

    return redirect(url_for('admin.list_roles'))


@admin.route('/users')
@login_required
def list_users():
    """
    List all users
    """
    check_admin()

    users = User.query.all()
    return render_template('admin/users/users.html',
                           users=users,
                           title='Users')


@admin.route('/users/add', methods=['GET', 'POST'])
@login_required
def add_user():
    """
    Add a user
    """
    check_admin()

    add_user = True
    user = User()
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    middle_name=form.middle_name.data,
                    password=form.password.data,
                    role_id=form.role.data.id,
                    tel=form.tell.data)

        db.session.add(user)
        db.session.commit()
        flash('You have successfully add user.')

        # redirect to the user list PAGE
        return redirect(url_for('admin.list_users'))

    return render_template('admin/users/user.html',
                           user=user,
                           form=form,
                           title='Add User',
                           add_user=add_user)


@admin.route('/users/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_user(id):
    """
    Delete a user
    """
    check_admin()

    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    flash('You have successfully deleted the user.')

    # redirect to the user list PAGE
    return redirect(url_for('admin.list_users'))


@admin.route('/users/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_user(id):
    """
    Change user information
    """
    check_admin()

    add_user = False

    user = User.query.get_or_404(id)

    form = UserEditForm(obj=user)
    if form.validate_on_submit():
        user.role_id = form.role.data.id
        user.username = form.username.data
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.middle_name = form.middle_name.data
        user.email = form.email.data
        user.tel = form.tell.data
        db.session.add(user)
        db.session.commit()
        flash('You have successfully assigned a role.')

        # redirect to the user list PAGE
        return redirect(url_for('admin.list_users'))

    form.username.data = user.username
    form.first_name.data = user.first_name
    form.last_name.data = user.last_name
    form.middle_name.data = user.middle_name
    form.email.data = user.email
    form.tell.data = user.tel
    form.role.data = Role.query.get_or_404(user.role_id)

    return render_template('admin/users/user.html',
                           user=user,
                           form=form,
                           title='Edit User',
                           add_user=add_user)


@admin.route('/class_specializations')
@login_required
def list_class_specializations():
    """
    Show the list of specializations of classes
    """
    check_admin()

    specializations = Specialization.query.all()
    return render_template('admin/class_specializations/class_specializations.html',
                           specializations=specializations)


@admin.route('/class_specializations/add', methods=['GET', 'POST'])
@login_required
def add_class_specializations():
    """
    Add class specialization
    """
    check_admin()

    add_specialization = True

    form = SpecializationForm()
    if form.validate_on_submit():
        specialization = Specialization(name=form.name.data)

        try:
            db.session.add(specialization)
            db.session.commit()
            flash('You have successfully added a new specialization.')
        except:
            flash('Error: specialization name already exists.')

        # redirect to the list of specializations of classes PAGE
        return redirect(url_for('admin.list_class_specializations'))

    return render_template('admin/class_specializations/class_specialization.html',
                           add_specialization=add_specialization,
                           form=form,
                           title='Add Class Specialization')


@admin.route('/class_specializations/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_class_specializations(id):
    """
    Delete class specialization
    """
    check_admin()

    specialization = Specialization.query.get_or_404(id)
    db.session.delete(specialization)
    db.session.commit()
    flash('You have successfully deleted the specialization.')

    # redirect to the list of specializations of classes PAGE
    return redirect(url_for('admin.list_class_specializations'))


@admin.route('/class_specializations/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_class_specializations(id):
    """
    Edit class specialization
    """
    check_admin()

    add_specialization = False

    specialization = Specialization.query.get_or_404(id)
    form = SpecializationForm(obj=specialization)
    if form.validate_on_submit():
        specialization.name = form.name.data
        db.session.add(specialization)
        db.session.commit()
        flash('You have successfully edited the specialization.')

        # redirect to the list of specializations of classes PAGE
        return redirect(url_for('admin.list_class_specializations'))

    form.name.data = specialization.name
    return render_template('admin/class_specializations/class_specialization.html',
                           add_specialization=add_specialization,
                           form=form,
                           title="Edit Class Specialization")


@admin.route('/room_specializations')
@login_required
def list_room_specializations():
    """
    Show the list of specializations of classroom
    """
    check_admin()

    room_specializations = RoomSpecialization.query.all()
    return render_template('admin/room_specializations/room_specializations.html',
                           room_specializations=room_specializations, )


@admin.route('/room_specializations/add', methods=['GET', 'POST'])
@login_required
def add_room_specializations():
    """
    Add classroom specialization
    """
    check_admin()

    add_room_specialization = True

    form = SpecializationForm()
    if form.validate_on_submit():
        room_specialization = RoomSpecialization(name=form.name.data)

        try:
            db.session.add(room_specialization)
            db.session.commit()
            flash('You have successfully added a new classroom specialization.')
        except:
            flash('Error: class specialization name already exists.')

        # redirect to the list of specializations of classroom PAGE
        return redirect(url_for('admin.list_room_specializations'))

    return render_template('admin/room_specializations/room_specialization.html',
                           add_room_specialization=add_room_specialization,
                           form=form,
                           title='Add Room Specialization')


@admin.route('/room_specializations/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_room_specialization(id):
    """
    Delete classroom specialization
    """
    check_admin()

    room_specializations = RoomSpecialization.query.get_or_404(id)
    db.session.delete(room_specializations)
    db.session.commit()
    flash('You have successfully deleted the classroom specialization.')

    # redirect to the list of specializations of classroom PAGE
    return redirect(url_for('admin.list_room_specializations'))


@admin.route('/room_specializations/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_room_specializations(id):
    """
    Edit classroom specialization
    """
    check_admin()

    add_room_specialization = False

    room_specialization = RoomSpecialization.query.get_or_404(id)
    form = SpecializationForm(obj=room_specialization)
    if form.validate_on_submit():
        room_specialization.name = form.name.data
        db.session.add(room_specialization)
        db.session.commit()
        flash('You have successfully edited the room specialization.')

        # redirect to the list of specializations of classroom PAGE
        return redirect(url_for('admin.list_room_specializations'))

    form.name.data = room_specialization.name
    return render_template('admin/room_specializations/room_specialization.html',
                           add_room_specialization=add_room_specialization,
                           form=form,
                           title="Edit Room Specialization")


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


@admin.route('/students_class')
@login_required
def list_students_class():
    """
    A list link between students and class
    """
    check_admin()

    students = User.query.filter_by(role_id=2).outerjoin(StudentInClass, User.id==StudentInClass.user_id_studen).all()

    return render_template('admin/students/list.html',
                           students=students)


@admin.route('/students_class/add', methods=['GET', 'POST'])
@login_required
def add_students_class():
    """
    Add link between students and class
    """
    check_admin()

    form = StudentToClassAddForm()
    if form.validate_on_submit():
        student_to_class = StudentInClass(class_id=form.class_name.data.id,
                                          user_id_studen=form.student.data.id)

        try:
            db.session.add(student_to_class)
            db.session.commit()
            flash('You have successfully added a new link between student and class.')
        except:
            flash('Error')

        # redirect to the list links between students and class PAGE
        return redirect(url_for('admin.list_students_class'))

    form.student.query = db.session.query(User).filter(User.role_id == 2).outerjoin(StudentInClass).filter(
        StudentInClass.class_id == None)
    return render_template('admin/students/edit.html',
                           form=form,
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

    edit_student_to_class = True

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
                           edit_student_to_class=edit_student_to_class,
                           title='Edit link between student and class')