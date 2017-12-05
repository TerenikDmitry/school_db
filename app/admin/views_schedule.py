from . import admin, check_admin
from .. import db

from flask import render_template, flash, redirect, url_for
from flask_login import login_required

from forms import ScheduleForm

from ..models import Schedule, EducationPlan, Classroom, Class, TeacherToSubject


@admin.route('/schedule')
@login_required
def list_schedule():
    """
    Show schedule
    """
    check_admin()

    #User.query.filter_by(role_id=2).outerjoin(StudentInClass, StudentInClass.user_id_studen == User.id).filter(
    #    StudentInClass.class_id == None)

    plans = []
    for planY in EducationPlan.query.distinct(EducationPlan.year):
        for plan in EducationPlan.query.filter_by(year=planY.year).distinct(EducationPlan.semester):
            plans.append({'_year':planY.year,'_semester':plan.semester})

    return render_template('admin/schedule/mainList.html',
                           plans=plans)


@admin.route('/schedule/<int:year>/<int:semester>')
@login_required
def list_schedule_year_sem(year,semester):
    """
    Show schedule
    """
    check_admin()

    schedules = EducationPlan.query.filter(EducationPlan.year==year, EducationPlan.semester==semester).order_by(EducationPlan.day, EducationPlan.lessonNumber).all()

    test = schedules[0].schedule_id.all()
    return render_template('admin/schedule/list.html',
                           schedules=schedules)


@admin.route('/schedule/<int:year>/<int:semester>/<int:plan_id>/edit')
@login_required
def edit_schedule_year_sem(plan_id,year,semester):
    """
    Edit schedule
    """
    check_admin()

    schedules = Schedule.query.filter_by(educationPlan_id=plan_id).first()
    form = ScheduleForm(obj=schedules)
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
        return redirect(url_for('admin.list_schedule_year_sem', year=year, semester=semester))

    form.classroom_id.data = Classroom.query.get_or_404(schedules.classroom_id)
    form.class_id.data = Class.query.get_or_404(schedules.class_id)
    form.teacher_subject_id.data = TeacherToSubject.query.get_or_404(schedules.teacher_subject_id)
    return render_template('admin/schedule/edit.html',
                           form=form,
                           plan=EducationPlan.query.get_or_404(plan_id),
                           title="Edit Schedule")


@admin.route('/schedule/<int:year>/<int:semester>/<int:id>/delete')
@login_required
def delete_schedule_year_sem(id,year,semester):
    """
    Show schedule
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
    return redirect(url_for('admin.list_schedule_year_sem', year=year, semester=semester))