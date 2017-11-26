from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired
from ..models import Classroom, Specialization, User


class ClassForm(FlaskForm):
    """
    Form for admin to add or edit a role
    """
    name = StringField('Name', validators=[DataRequired()])
    date_start = DateField('DateStart', validators=[DataRequired()])
    date_end = DateField('DateEnd', validators=[DataRequired()])
    specialization_id = QuerySelectField(query_factory=lambda: Specialization.query.all(), get_label="name")
    head_teacher_id = QuerySelectField(query_factory=lambda: User.query.filter_by(role_id=1).all(), get_label="last_name")
    classroom_id = QuerySelectField(query_factory=lambda: Classroom.query.all(), get_label="name")
    submit = SubmitField('Submit')