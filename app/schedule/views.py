from datetime import date

from sqlalchemy.orm.exc import NoResultFound

from . import schedule

from flask import render_template
from flask_login import login_required

from ..models import Schedule, EducationPlan, Class


def curr_year():
    return date.today().year


def curr_semester():
    month = date.today().month
    if 9 <= month <= 12:
        return 1
    else:
        return 2


@schedule.route('/schedule/class/<int:id_class>/day/<int:id_day>')
@login_required
def list_schedule_class(id_class, id_day):
    """
    Show schedule for some class
    """

    schedules = []

    current_class = Class.query.get_or_404(id_class)

    plans = EducationPlan.query.filter_by(year=curr_year(), semester=curr_semester(), day=id_day).order_by(
        EducationPlan.year, EducationPlan.semester, EducationPlan.day, EducationPlan.lessonNumber).all()
    for plan in plans:
        try:
            schedule_element = Schedule.query.filter_by(educationPlan_id=plan.id, class_id=id_class).one()
            schedules.append(schedule_element)
        except NoResultFound:
            schedules.append(plan)

    plans_day = EducationPlan.query.filter_by(year=curr_year(), semester=curr_semester()).distinct(EducationPlan.day)

    return render_template('schedule/dayClassList.html',
                           currentClass=current_class,
                           schedules=schedules,
                           currentDay=plans[0],
                           days=plans_day,
                           title='Schedule')
