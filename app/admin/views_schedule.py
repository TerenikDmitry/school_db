from datetime import date

from flask_sqlalchemy import Pagination
from sqlalchemy.orm.exc import NoResultFound

from . import admin, check_admin
from .. import db

from flask import render_template, flash, redirect, url_for, abort
from flask_login import login_required, current_user

from sqlalchemy import desc

from .forms import ScheduleFormEdit, ScheduleFormAdd, ScheduleFormAddSubject

from ..models import Schedule, EducationPlan, Classroom, Class, TeacherToSubject


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


@admin.route('/schedule')
@login_required
def list_schedule():
    """
    Show schedule
    """
    user_access()

    plans = []
    for plans_year in EducationPlan.query.distinct(EducationPlan.year).order_by(desc(EducationPlan.year)):
        for plans_semester in EducationPlan.query.filter_by(year=plans_year.year).distinct(EducationPlan.semester):
            plans.append({'_year':plans_year.year,'_semester':plans_semester.semester})

    return render_template('admin/schedule/mainList.html',
                           plans=plans,
                           title='Schedules')


@admin.route('/schedule/teacher/<int:id_subject>/<int:id_day>')
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

    return render_template('admin/schedule/dayTeacherList.html',
                           teacherSubject=teacher_subject,
                           schedules=schedules,
                           day=all_plans[0],
                           plans=plans,
                           title='Schedule')


@admin.route('/schedule/<int:id_plan>/<int:id_subject>/<int:id_day>/add', methods=['GET', 'POST'])
@login_required
def add_schedule_subject(id_subject, id_day, id_plan):
    """
    Add schedule
    """
    user_access()

    form = ScheduleFormAddSubject()
    if form.validate_on_submit():
        try:
            schedule = Schedule(classroom_id=form.classroom_id.data.id,
                                class_id=form.class_id.data.id,
                                teacher_subject_id=id_subject,
                                educationPlan_id=id_plan)
            db.session.add(schedule)
            db.session.commit()
            flash('You have successfully added Schedule.', category='message')
        except:
            flash('Error in adding Schedule.', category='error')

        # redirect to the list roles PAGE
        return redirect(url_for('admin.list_schedule_teacher', id_subject=id_subject, id_day=id_day))

    return render_template('admin/schedule/edit.html',
                           form=form,
                           title="Add Schedule")


@admin.route('/schedule/subject/<int:id_subject>/<int:id_day>/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def delete_schedule_subject(id_subject, id_day, id):
    """
    Delete schedule
    """
    user_access()

    schedules = Schedule.query.get_or_404(id)
    try:
        db.session.delete(schedules)
        db.session.commit()
        flash('You have successfully deleted the Schedule.', category='message')
    except:
        flash('Error in removing Schedule.', category='error')

    # redirect to the list roles PAGE
    return redirect(url_for('admin.list_schedule_subject',id_subject=id_subject, id_day=id_day))


@admin.route('/schedule/<int:year>/<int:semester>/<int:pagin>')
@login_required
def list_schedule_year_sem(year, semester, pagin):
    """
    Show schedule
    """
    user_access()

    schedules = Schedule.query.outerjoin(EducationPlan, EducationPlan.id==Schedule.educationPlan_id).filter(EducationPlan.year==year, EducationPlan.semester==semester).order_by(EducationPlan.day, EducationPlan.lessonNumber).paginate(page=pagin, per_page=10)

    return render_template('admin/schedule/yearSemesterList.html',
                           schedules=schedules,
                           year=year,
                           semester=semester,
                           title='Schedules')


@admin.route('/schedule/<int:year>/<int:semester>/add', methods=['GET', 'POST'])
@login_required
def add_schedule_year_sem(year, semester):
    """
    Add schedule
    """
    check_admin()

    form = ScheduleFormAdd()
    if form.validate_on_submit():
        try:
            schedule = Schedule(classroom_id=form.classroom_id.data.id,
                                class_id=form.class_id.data.id,
                                teacher_subject_id=form.teacher_subject_id.data.id,
                                educationPlan_id=form.educationPlan_id.data.id)
            db.session.add(schedule)
            db.session.commit()
            flash('You have successfully added Schedule.', category='message')
        except:
            flash('Error in adding Schedule.', category='error')

        # redirect to the list roles PAGE
        return redirect(url_for('admin.list_schedule_year_sem', year=year, semester=semester, pagin=1))

    form.educationPlan_id.query = EducationPlan.query.filter(EducationPlan.year==year, EducationPlan.semester==semester)
    return render_template('admin/schedule/edit.html',
                           form=form,
                           title="Add Schedule")


@admin.route('/schedule/<int:year>/<int:semester>/<int:plan_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_schedule_year_sem(plan_id, year, semester):
    """
    Edit schedule
    """
    check_admin()

    schedules = Schedule.query.filter_by(educationPlan_id=plan_id).first()
    form = ScheduleFormEdit(obj=schedules)
    if form.validate_on_submit():
        try:
            schedules.classroom_id = form.classroom_id.data.id
            schedules.class_id = form.class_id.data.id
            schedules.teacher_subject_id = form.teacher_subject_id.data.id
            db.session.add(schedules)
            db.session.commit()
            flash('You have successfully edited Schedule.', category='message')
        except:
            flash('Error in changing Schedule.', category='error')

        # redirect to the list roles PAGE
        return redirect(url_for('admin.list_schedule_year_sem', year=year, semester=semester, pagin=1))

    form.classroom_id.data = Classroom.query.get_or_404(schedules.classroom_id)
    form.class_id.data = Class.query.get_or_404(schedules.class_id)
    form.teacher_subject_id.data = TeacherToSubject.query.get_or_404(schedules.teacher_subject_id)
    return render_template('admin/schedule/edit.html',
                           form=form,
                           plan=EducationPlan.query.get_or_404(plan_id),
                           title="Edit Schedule")


@admin.route('/schedule/<int:year>/<int:semester>/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def delete_schedule_year_sem(id, year, semester):
    """
    Delete schedule
    """
    check_admin()

    schedules = Schedule.query.get_or_404(id)
    try:
        db.session.delete(schedules)
        db.session.commit()
        flash('You have successfully deleted the Schedule.', category='message')
    except:
        flash('Error in removing Schedule.', category='error')

    # redirect to the list roles PAGE
    return redirect(url_for('admin.list_schedule_year_sem', year=year, semester=semester, pagin=1))