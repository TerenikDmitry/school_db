import datetime
from flask_login import UserMixin
from sqlalchemy import UniqueConstraint, CheckConstraint
from sqlalchemy.ext.hybrid import hybrid_property
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager


class User(UserMixin, db.Model):
    """
    Users table
    """

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True, unique=True)
    username = db.Column(db.String(60), index=True, unique=True)
    tel = db.Column(db.String(60), default='-')
    first_name = db.Column(db.String(60), index=True, nullable=False)
    last_name = db.Column(db.String(60), index=True, nullable=False)
    middle_name = db.Column(db.String(60), index=True)
    password_hash = db.Column(db.String(128), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    studentInClass = db.relationship('StudentInClass', backref='users', lazy='dynamic', cascade="all, delete")
    teacherInClass = db.relationship('Class', backref='users', lazy='dynamic', cascade="all, delete")
    teacherToSubject = db.relationship('TeacherToSubject', backref='users', lazy='dynamic', cascade="all, delete")
    teacherClassroom = db.relationship('TeachersClassroom', backref='users', lazy='dynamic', cascade="all, delete")
    schedule_id = db.relationship('Schedule', backref='users', lazy='dynamic')
    grade_id = db.relationship('Grade', backref='users', lazy='dynamic')

    @property
    def password(self):
        """
        Prevent password from being accessed
        """
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        return check_password_hash(self.password_hash, password)

    @hybrid_property
    def fullname(self):
        return self.last_name + " " + self.first_name + " " + self.middle_name

    def __repr__(self):
        return '{}: {} {} {}'.format(self.id, self.last_name, self.first_name, self.middle_name)


# Set up user_loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Role(db.Model):
    """
    Role table
    """

    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200), default='-')

    user_id = db.relationship('User', backref='roles', lazy='dynamic', cascade="all, delete-orphan")

    def __repr__(self):
        return '<Role: {}>'.format(self.name)


class StudentInClass(db.Model):
    """
    Specialization table
    """

    __tablename__ = 'students_in_class'

    id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'))
    user_id_studen = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return '<StudentInClass: {}>'.format(self.name)


class Class(db.Model):
    """
    Class table
    """

    __tablename__ = 'classes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    dateStartEducation = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    dateEndEducation = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    specialization_id = db.Column(db.Integer, db.ForeignKey('specializations.id'), nullable=False)
    headTeacher = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('classrooms.id'), nullable=False)

    students = db.relationship('StudentInClass', backref='classes', lazy='dynamic',cascade="all, delete")
    schedule_id = db.relationship('Schedule', backref='classes', lazy='dynamic')

    def __repr__(self):
        return '<Class: {}>'.format(self.name)

    def __str__(self):
        return '{}'.format(self.name)


class Specialization(db.Model):
    """
    Specialization table
    """

    __tablename__ = 'specializations'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)

    specialization_id = db.relationship('Class', backref='specializations', lazy='dynamic')

    def __repr__(self):
        return '<Specialization: {}>'.format(self.name)

    def __str__(self):
        return '{}'.format(self.name)


class Subject(db.Model):
    """
    Subject table
    """

    __tablename__ = 'subjects'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)

    teacher_subject_id = db.relationship('TeacherToSubject', backref='subjects', lazy='dynamic')
    schedule_id = db.relationship('Schedule', backref='subjects', lazy='dynamic')

    def __repr__(self):
        return '<Subject: {}>'.format(self.name)

    def __str__(self):
        return '{}'.format(self.name)


class TeacherToSubject(db.Model):
    """
    Specialization table
    """

    __tablename__ = 'teachers_to_subjects'

    id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'))
    user_id_teacher = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return '<TeacherToSubject: teacher {} - subject {}>'.format(self.user_id_teacher, self.subject_id)


class RoomSpecialization(db.Model):
    """
        Room Specialization table
    """

    __tablename__ = 'room_specializations'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)

    room_specialization_id = db.relationship('Classroom', backref='room_specializations', lazy='dynamic')

    def __repr__(self):
        return '<Room Specialization: {}>'.format(self.name)


class Classroom(db.Model):
    """
        Classroom table
    """

    __tablename__ = 'classrooms'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    room_specialization_id = db.Column(db.Integer, db.ForeignKey('room_specializations.id'), nullable=False)

    classroom_id = db.relationship('Class', backref='classrooms', lazy='dynamic')
    teacher_id = db.relationship('TeachersClassroom', backref='classrooms', lazy='dynamic', cascade="all, delete")
    schedule_id = db.relationship('Schedule', backref='classrooms', lazy='dynamic')

    def __repr__(self):
        return '<Classroom: {}>'.format(self.name)

    def __str__(self):
        return '{}'.format(self.name)


class ParentToStudent(db.Model):
    """
    ParentToStudent table
    """

    __tablename__ = 'parents_to_student'
    __table_args__ = (UniqueConstraint('user_id_parent', 'user_id_student', name='_student_parents'),)

    id = db.Column(db.Integer, primary_key=True)
    user_id_parent = db.Column(db.Integer, db.ForeignKey('users.id'))
    user_id_student = db.Column(db.Integer, db.ForeignKey('users.id'))

    parentStudent = db.relationship('User', foreign_keys=user_id_parent)
    studentParent = db.relationship('User', foreign_keys=user_id_student)

    def __repr__(self):
        return '<ParentToStudent: parent {} - student {}>'.format(self.user_id_parent, self.user_id_studen)


class TypeOfWork(db.Model):
    """
    TypeOfWork table
    """

    __tablename__ = 'types_of_work'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)

    grade_id = db.relationship('Grade', backref='types_of_work', lazy='dynamic')

    def __repr__(self):
        return '<TypeOfWork: {}>'.format(self.name)


class EducationPlan(db.Model):
    """
    EducationPlan table
    """

    __tablename__ = 'education_plan'
    __table_args__ = (
        CheckConstraint('CHECK (day >= 0)'),
        CheckConstraint('CHECK (day <= 6)'),
        CheckConstraint('CHECK (lessonNumber >= 0)'),
        CheckConstraint('CHECK (lessonNumber <= 6)'),
        CheckConstraint('CHECK (semester >= 1)'),
        CheckConstraint('CHECK (semester <= 2)'),
        CheckConstraint('year' <= (datetime.date.today().year + 2)),
    )

    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.Integer, default=0)
    year = db.Column(db.Integer, default=(datetime.date.today().year + 1))
    lessonNumber = db.Column(db.Integer, default=0)
    semester = db.Column(db.Integer, default=0)

    schedule_id = db.relationship('Schedule', backref='education_plan', lazy='dynamic')

    def __repr__(self):
        return '<EducationPlan: year {}, semester {}>'.format(self.year, self.semester)


class TeachersClassroom(db.Model):
    """
    TeachersClassroom table
    """

    __tablename__ = 'teachers_classroom'

    id = db.Column(db.Integer, primary_key=True)
    classroom_id = db.Column(db.Integer, db.ForeignKey('classrooms.id'))
    user_id_teacher = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True)

    def __repr__(self):
        return '<TeachersClassroom: teacher:{} - classroom:{}>'.format(self.user_id_teacher,self.classroom_id)


class Schedule(db.Model):
    """
    Schedule table
    """

    __tablename__ = 'schedules'

    id = db.Column(db.Integer, primary_key=True)
    classroom_id = db.Column(db.Integer, db.ForeignKey('classrooms.id'))
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'))
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'))
    teacher_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    educationPlan_id = db.Column(db.Integer, db.ForeignKey('education_plan.id'))

    grade_id = db.relationship('Grade', backref='schedules', lazy='dynamic')

    def __repr__(self):
        return '<Schedule: {}>'.format(self.id)


class Grade(db.Model):
    """
    Grades table
    """

    __tablename__ = 'grades'

    id = db.Column(db.Integer, primary_key=True)
    grade = db.Column(db.Integer, nullable=False)
    typeOfWork_id = db.Column(db.Integer, db.ForeignKey('types_of_work.id'))
    schedule_id = db.Column(db.Integer, db.ForeignKey('schedules.id'))
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return '<Grade: student:{} grade:{}>'.format(self.student_id, self.grade)