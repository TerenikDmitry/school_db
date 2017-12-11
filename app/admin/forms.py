import datetime

from flask_wtf import FlaskForm

from wtforms import StringField, SubmitField, PasswordField, ValidationError, IntegerField, SelectField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, NumberRange
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from ..models import Role, User, RoomSpecialization, Class, Subject, Classroom, EducationPlan, TeacherToSubject


class RoleForm(FlaskForm):
    """
    Form for admin to add or edit a role
    """
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')


class SpecializationForm(FlaskForm):
    """
    Form for admin to add or edit a role
    """
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Submit')


class UserEditForm(FlaskForm):
    """
    Form for admin to assign departments and roles to employees
    """
    username = StringField('Login', validators=[DataRequired()])
    email = StringField('Mail', validators=[DataRequired(), Email()])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    middle_name = StringField('Middle Name', validators=[DataRequired()])
    telephone = StringField('Telephone')
    is_man = BooleanField('Is man')
    submit = SubmitField('Submit')


class RegistrationForm(FlaskForm):
    """
    Form for users to create new account
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    middle_name = StringField('Middle Name', validators=[DataRequired()])
    telephone = StringField('Telephone')
    password = PasswordField('Password', validators=[
        DataRequired(),
        EqualTo('confirm_password')
    ])
    confirm_password = PasswordField('Confirm Password')
    is_man = BooleanField('Is man')
    role = QuerySelectField(query_factory=lambda: Role.query.all(), get_label="name")
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email is already in use.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username is already in use.')


class UserAddForm(FlaskForm):
    """
    Form for admin to assign departments and roles to employees
    """
    login = StringField('Login*', validators=[DataRequired()])
    email = StringField('Mail*', validators=[DataRequired(), Email()])
    password = PasswordField('Password*', validators=[DataRequired()])
    first_name = StringField('First Name*', validators=[DataRequired()])
    last_name = StringField('Last Name*', validators=[DataRequired()])
    middle_name = StringField('Middle Name*', validators=[DataRequired()])
    tell = StringField('Telephone')
    role = QuerySelectField(query_factory=lambda: Role.query.all(),
                            get_label="name")
    is_man = BooleanField('Sex')
    submit = SubmitField('Submit')


class ClassroomEditForm(FlaskForm):
    """
    Form for admin to assign departments and roles to employees
    """
    name = StringField('Name', validators=[DataRequired()])
    spec = QuerySelectField(query_factory=lambda: RoomSpecialization.query.all(),
                            get_label="name")
    submit = SubmitField('Submit')


def get_users():
    return User.query


def get_classes():
    return Class.query


def get_subjects():
    return Subject.query


def get_classrooms():
    return Classroom.query


class ParentToStudentAddForm(FlaskForm):
    """
    Form for admin to edit link between parents and students
    """
    parent = QuerySelectField(query_factory=get_users)
    student = QuerySelectField(query_factory=get_users)
    submit = SubmitField('Submit')


class ParentToStudentEditForm(FlaskForm):
    """
    Form for admin to edit student link between parents and students
    """
    student = QuerySelectField(query_factory=get_users)
    submit = SubmitField('Submit')


class StudentToClassEditForm(FlaskForm):
    """
    Form for admin to edit student link between parents and students
    """
    class_name = QuerySelectField(query_factory=get_classes)
    submit = SubmitField('Submit')


class TeacherSubjectAddForm(FlaskForm):
    """
        Form for admin to add link between teacher and subject
    """
    subject = QuerySelectField(query_factory=get_subjects)
    submit = SubmitField('Submit')


class TeacherClassroomEditForm(FlaskForm):
    """
        Form for admin to add link between teacher and classroom
    """
    classroom = QuerySelectField(query_factory=get_classrooms)
    submit = SubmitField('Submit')


class PlanForm(FlaskForm):
    """
        Form for admin to add one Plan
    """
    year = IntegerField('Year', [NumberRange(min=1996, max=2017, message=None)], default=(datetime.date.today().year))
    semester = SelectField('Semester', choices=[(1, '1 semester'), (2, '2 semester')], coerce=int)
    day = SelectField('Day', coerce=int, choices=[(1, 'Monday'),
                                       (2, 'Tuesday'),
                                       (3, 'Wednesday'),
                                       (4, 'Thursday'),
                                       (5, 'Friday'),
                                       (6, 'Saturday'),
                                       (7, 'Sunday')
                                       ])
    lessonNumber = SelectField('Lesson number', coerce=int,choices = [(g, '{} lesson'.format(g)) for g in range(1,8)])
    submit = SubmitField('Submit')


class PlanFormDay(FlaskForm):
    """
        Form for admin to add Plan to all day
    """
    year = IntegerField('Year', [NumberRange(min=1996, max=2017, message=None)], default=(datetime.date.today().year))
    semester = SelectField('Semester', choices=[(1, '1 semester'), (2, '2 semester')], coerce=int)
    day = SelectField('Day', coerce=int, choices=[(1, 'Monday'),
                                       (2, 'Tuesday'),
                                       (3, 'Wednesday'),
                                       (4, 'Thursday'),
                                       (5, 'Friday'),
                                       (6, 'Saturday'),
                                       (7, 'Sunday')
                                       ])
    submit = SubmitField('Submit')


class PlanFormSemester(FlaskForm):
    """
        Form for admin to add Plan to all semester
    """
    year = IntegerField('Year', [NumberRange(min=1996, max=2017, message=None)], default=(datetime.date.today().year))
    semester = SelectField('Semester', choices=[(1, '1 semester'), (2, '2 semester')], coerce=int)
    submit = SubmitField('Submit')


class ScheduleFormEdit(FlaskForm):
    """
        Form for admin to edit Schedule
    """
    classroom_id = QuerySelectField(query_factory=lambda: Classroom.query)
    class_id = QuerySelectField(query_factory=lambda: Class.query)
    teacher_subject_id = QuerySelectField(query_factory=lambda: TeacherToSubject.query.all())
    submit = SubmitField('Submit')


class ScheduleFormAdd(FlaskForm):
    """
        Form for admin to add Schedule
    """
    classroom_id = QuerySelectField(query_factory=lambda: Classroom.query)
    class_id = QuerySelectField(query_factory=lambda: Class.query)
    teacher_subject_id = QuerySelectField(query_factory=lambda: TeacherToSubject.query.all())
    educationPlan_id = QuerySelectField(query_factory=lambda: EducationPlan.query.order_by(EducationPlan.year,EducationPlan.semester).all())
    submit = SubmitField('Submit')


class ScheduleFormAddSubject(FlaskForm):
    """
        Form for admin to add Schedule
    """
    classroom_id = QuerySelectField(query_factory=lambda: Classroom.query)
    class_id = QuerySelectField(query_factory=lambda: Class.query)
    submit = SubmitField('Submit')