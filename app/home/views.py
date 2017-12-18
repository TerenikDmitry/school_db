from flask import abort, render_template, flash
from flask_login import current_user, login_required

from ..models import Role, User, TeacherToSubject, ParentToStudent, TeachersClassroom, Class, StudentInClass

from . import home


def check_admin():
    """
    Prevent non-admins from accessing the page
    """
    if not current_user.is_admin:
        abort(403)


def check_student(role_id):
    role = Role.query.get_or_404(role_id)

    if role.name != "Student":
        abort(403)


def check_teacher(role_id):
    role = Role.query.get_or_404(role_id)

    if role.name != "Teacher":
        abort(403)


def check_parent(role_id):
    role = Role.query.get_or_404(role_id)

    if role.name != "Parent":
        abort(403)


@home.route('/')
@home.route('/dashboard')
@login_required
def homepage():
    return render_template('home/index.html',
                           title="Welcome")


@home.route('/admin')
@login_required
def admin_dashboard():
    # prevent non-admins from accessing the page
    check_admin()

    return render_template('home/admin_dashboard.html', title="Dashboard")


@home.route('/class/<int:id>')
@login_required
def class_dashboard(id):
    classStudents = StudentInClass.query.filter_by(class_id=id).all()
    _class = Class.query.get_or_404(id)

    if current_user.role_id == 1 or current_user.role_id == 2:
        return render_template('home/class_dashboard.html',
                               title='Class',
                               _class=_class,
                               classStudents=classStudents)
    else:
        return render_template('home/class_dashboard_all.html',
                               title='Class',
                               _class=_class,
                               classStudents=classStudents)


@home.route('/student/<int:id>')
@login_required
def student_dashboard(id):
    user = User.query.get_or_404(id)

    check_student(user.role_id)

    parents = ParentToStudent.query.filter_by(user_id_student=id).all()

    studentClass = user.studentInClass.first()

    if current_user.role_id == 1 or current_user.role_id == 2:
        return render_template('home/student_dashboard.html',
                               user=user,
                               studentClass=studentClass,
                               parents=parents)
    else:
        return render_template('home/student_dashboard_all.html',
                               user=user,
                               studentClass=studentClass,
                               parents=parents)


@home.route('/teacher/<int:id>')
@login_required
def teacher_dashboard(id):
    user = User.query.get_or_404(id)

    check_teacher(user.role_id)

    headClass = Class.query.filter_by(headTeacher=id).first()

    subjects = TeacherToSubject.query.filter_by(user_id_teacher=id).all()

    classroom = TeachersClassroom.query.filter_by(user_id_teacher=id).first()

    if current_user.role_id == 1 or current_user.is_admin:
        return render_template('home/teacher_dashboard.html',
                               user=user,
                               headClass=headClass,
                               subjects=subjects,
                               classroom=classroom)
    else:
        return render_template('home/teacher_dashboard_all.html',
                               user=user,
                               headClass=headClass,
                               subjects=subjects,
                               classroom=classroom)


@home.route('/parent/<int:id>')
@login_required
def parent_dashboard(id):
    user = User.query.get_or_404(id)

    check_parent(user.role_id)

    childrens = ParentToStudent.query.filter_by(user_id_parent=id).all()

    return render_template('home/parent_dashboard.html',
                           user=user,
                           childrens=childrens)