from datetime import date

from sqlalchemy.orm.exc import NoResultFound

from . import schedule

from flask import render_template, abort
from flask_login import login_required, current_user

from ..models import Schedule, EducationPlan, Class, TeacherToSubject


def user_access():
    if not (current_user.role_id == 1 or current_user.is_admin):
        abort(403)


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


@schedule.route('/schedule/teacher/<int:id_subject>/day/<int:id_day>')
@login_required
def list_schedule_teacher(id_subject, id_day):
    """
    Show schedule
    """
    user_access()

    schedules = []
    teacher_subject = TeacherToSubject.query.get_or_404(id_subject)

    all_plans = EducationPlan.query.filter_by(year=curr_year(),semester=curr_semester(),day=id_day).order_by(EducationPlan.year, EducationPlan.semester, EducationPlan.day, EducationPlan.lessonNumber).all()
    for one_plan in all_plans:
        try:
            schedule = Schedule.query.filter_by(educationPlan_id=one_plan.id,teacher_subject_id=id_subject).one()
            schedules.append(schedule)
        except NoResultFound:
            schedules.append(one_plan)

    plans = EducationPlan.query.filter_by(year=curr_year(),semester=curr_semester()).distinct(EducationPlan.day)

    return render_template('schedule/dayTeacherList.html',
                           teacherSubject=teacher_subject,
                           schedules=schedules,
                           day=all_plans[0],
                           plans=plans,
                           title='Schedule')