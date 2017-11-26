from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from ..models import Role, User, RoomSpecialization


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
    tell = StringField('Telephone')
    role = QuerySelectField(query_factory=lambda: Role.query.all(), get_label="name")
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
    tell = PasswordField('Telephone')
    password = PasswordField('Password', validators=[
                                        DataRequired(),
                                        EqualTo('confirm_password')
                                        ])
    confirm_password = PasswordField('Confirm Password')
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