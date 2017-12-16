from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired
from ..models import Classroom, Specialization, User


class ClassForm(FlaskForm):
    """
    Form for admin to add or edit a class
    """
    name = StringField('Name', validators=[DataRequired()])
    dateStartEducation = DateField('DateStart', validators=[DataRequired()])
    dateEndEducation = DateField('DateEnd', validators=[DataRequired()])
    specialization_id = QuerySelectField(query_factory=lambda: Specialization.query.all())
    headTeacher = QuerySelectField(query_factory=lambda: User.query.filter_by(role_id=1).all())
    room_id = QuerySelectField(query_factory=lambda: Classroom.query.all())
    submit = SubmitField('Submit')


def get_students():
    return User.query


class ClassStudentsForm(FlaskForm):
    """
        Form for admin to add a student to class
    """
    student = QuerySelectField(query_factory=get_students)
    submit = SubmitField('Submit')