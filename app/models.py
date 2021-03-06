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
    email = db.Column(db.String(50), index=True, nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    first_name = db.Column(db.String(30), index=True, nullable=False)
    last_name = db.Column(db.String(30), index=True, nullable=False)
    middle_name = db.Column(db.String(30), index=True, nullable=False)
    date_of_birth = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    telephone = db.Column(db.String(20), nullable=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    is_man = db.Column(db.Boolean, nullable=False)

    studentInClass = db.relationship('StudentInClass', backref='users', lazy='dynamic', cascade="all, delete")
    teacherInClass = db.relationship('Class', backref='users', lazy='dynamic', cascade="all, delete")
    teacherToSubject = db.relationship('TeacherToSubject', backref='users', lazy='dynamic', cascade="all, delete")
    teacherClassroom = db.relationship('TeachersClassroom', backref='users', lazy='dynamic', cascade="all, delete")
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
        if len(password) <= 10:
            raise AttributeError('password must be longer than 10 characters')
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
        return '<User {}: {} {} {}>'.format(self.id, self.last_name, self.first_name, self.middle_name)

    def __str__(self):
        return '{}: {} {} {}'.format(self.id, self.last_name, self.first_name, self.middle_name)


# Set up user_loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def get_name_user(user_id):
    user = User.query.get(int(user_id))
    return user.fullname


def get_name_subject(id):
    subject = Subject.query.get(int(id))
    return subject.name


class Role(db.Model):
    """
    Role table
    """

    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    description = db.Column(db.String(400), nullable=True)

    user_id = db.relationship('User', backref='roles', lazy='dynamic', cascade="all, delete-orphan")

    def __repr__(self):
        return '<Role: {}>'.format(self.name)


class StudentInClass(db.Model):
    """
    Specialization table
    """

    __tablename__ = 'students_in_class'
    __table_args__ = (
        UniqueConstraint('class_id', 'user_id_studen', name='_studentClassUnique'),
    )

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
    name = db.Column(db.String(3), nullable=False, unique=True)
    dateStartEducation = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    dateEndEducation = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    specialization_id = db.Column(db.Integer, db.ForeignKey('specializations.id'), nullable=False)
    headTeacher = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('classrooms.id'), nullable=False)

    students = db.relationship('StudentInClass', backref='classes', lazy='dynamic',cascade="all, delete")
    schedule_id = db.relationship('Schedule', backref='classes', lazy='dynamic')

    def __repr__(self):
        return '<Class {}: {}>'.format(self.id, self.name)

    def __str__(self):
        return '{}'.format(self.name)


class Specialization(db.Model):
    """
    Specialization table
    """

    __tablename__ = 'specializations'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

    specialization_id = db.relationship('Class', backref='specializations', lazy='dynamic')

    def __repr__(self):
        return '<Specialization {}: {}>'.format(self.id, self.name)

    def __str__(self):
        return '{}'.format(self.name)


class Subject(db.Model):
    """
    Subject table
    """

    __tablename__ = 'subjects'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    teacher_subject_id = db.relationship('TeacherToSubject', backref='subjects', lazy='dynamic')

    def __repr__(self):
        return '<Subject {}: {}>'.format(self.id, self.name)

    def __str__(self):
        return '{}'.format(self.name)


class TeacherToSubject(db.Model):
    """
    Specialization table
    """

    __tablename__ = 'teachers_to_subjects'
    __table_args__ = (
        UniqueConstraint('subject_id', 'user_id_teacher', name='_teacherSubjectUnique'),
    )

    id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'))
    user_id_teacher = db.Column(db.Integer, db.ForeignKey('users.id'))

    schedule_id = db.relationship('Schedule', backref='teachers_to_subjects', lazy='dynamic')

    def __repr__(self):
        return '<TeacherToSubject: teacher {} - subject {}>'.format(self.user_id_teacher, self.subject_id)

    def __str__(self):
        return '{}: {} - {}'.format(self.id, get_name_user(self.user_id_teacher), get_name_subject(self.subject_id))


class RoomSpecialization(db.Model):
    """
        Room Specialization table
    """

    __tablename__ = 'room_specializations'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

    room_specialization_id = db.relationship('Classroom', backref='room_specializations', lazy='dynamic')

    def __repr__(self):
        return '<Room Specialization {}: {}>'.format(self.id, self.name)


class Classroom(db.Model):
    """
        Classroom table
    """

    __tablename__ = 'classrooms'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(5), nullable=False, unique=True)
    room_specialization_id = db.Column(db.Integer, db.ForeignKey('room_specializations.id'), nullable=False)

    classroom_id = db.relationship('Class', backref='classrooms', lazy='dynamic')
    teacher_id = db.relationship('TeachersClassroom', backref='classrooms', lazy='dynamic', cascade="all, delete")
    schedule_id = db.relationship('Schedule', backref='classrooms', lazy='dynamic')

    def __repr__(self):
        return '<Classroom {}: {}>'.format(self.id, self.name)

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
        UniqueConstraint('day', 'year', 'lessonNumber', 'semester', name='_plans'),
    )

    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.Integer, default=1)
    year = db.Column(db.Integer, default=(datetime.date.today().year + 1))
    lessonNumber = db.Column(db.Integer, default=1)
    semester = db.Column(db.Integer, default=1)

    schedule_id = db.relationship('Schedule', backref='education_plan', lazy='dynamic')

    @hybrid_property
    def dayLesson(self):
        days = {
            1: 'Monday',
            2: 'Tuesday',
            3: 'Wednesday',
            4: 'Thursday',
            5: 'Friday',
            6: 'Saturday',
            7: 'Sunday'
        }
        return '{}, {} lesson'.format(days[self.day], self.lessonNumber)

    @hybrid_property
    def fullday(self):
        days = {
            1: 'Monday',
            2: 'Tuesday',
            3: 'Wednesday',
            4: 'Thursday',
            5: 'Friday',
            6: 'Saturday',
            7: 'Sunday'
        }
        return days[self.day]

    def __repr__(self):
        return '<EducationPlan {}: year {}, semester {}, day {}, lesson number {}>'.format(self.id, self.year, self.semester, self.day, self.lessonNumber)

    def __str__(self):
        days = {
            1: 'Monday',
            2: 'Tuesday',
            3: 'Wednesday',
            4: 'Thursday',
            5: 'Friday',
            6: 'Saturday',
            7: 'Sunday'
        }
        return '{} year, {} semester, {}, {} lesson'.format(self.year, self.semester, days[self.day], self.lessonNumber)


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
    __table_args__ = (
        UniqueConstraint('class_id', 'educationPlan_id', name='_schedulesUnique'),
    )

    id = db.Column(db.Integer, primary_key=True)
    classroom_id = db.Column(db.Integer, db.ForeignKey('classrooms.id'))
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'))
    teacher_subject_id = db.Column(db.Integer, db.ForeignKey('teachers_to_subjects.id'))
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