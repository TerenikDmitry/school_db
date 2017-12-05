from . import *
from .. import db

from flask import render_template, flash, redirect, url_for
from flask_login import login_required

from forms import PlanForm, PlanFormDay
from ..models import EducationPlan

@admin.route('/plans')
@login_required
def list_plan():
    """
    Show plan list
    """
    check_admin()

    educationPlan = EducationPlan.query.order_by(EducationPlan.year, EducationPlan.semester, EducationPlan.day, EducationPlan.lessonNumber).all()
    return render_template('admin/plans/list.html',
                           educationPlan=educationPlan)


@admin.route('/plans/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def delete_plan(id):
    """
    Delete one plan
    """
    check_admin()

    try:
        plan = EducationPlan.query.get_or_404(id)
        db.session.delete(plan)
        db.session.commit()
        flash('You have successfully deleted the plan.',category='message')
    except:
        flash('Error. Delete the plan.',category='error')

    return redirect(url_for('admin.list_plan'))


@admin.route('/plans/add', methods=['GET', 'POST'])
@login_required
def add_plan():
    """
    Add one plan
    """
    check_admin()

    form = PlanForm()
    if form.validate_on_submit():
        plan = EducationPlan(year=form.year.data,
                             day=form.day.data,
                             lessonNumber=form.lessonNumber.data,
                             semester=form.semester.data)
        try:
            db.session.add(plan)
            db.session.commit()
            flash('You have successfully add the Plan.', category='message')
        except:
            flash('Such a Plan already exists.', category='error')

        return redirect(url_for('admin.list_plan'))

    return render_template('admin/plans/plan.html',
                           form=form,
                           title='Add Plan')


@admin.route('/plans/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_plan(id):
    """
    Edit one plan
    """
    check_admin()

    plan = EducationPlan.query.get_or_404(id)

    form = PlanForm(obj=plan)
    if form.validate_on_submit():
        try:
            db.session.add(plan)
            db.session.commit()
            flash('You have successfully edit the Plan.',category='message')
        except:
            flash('Error. Edit the Plan.', category='error')

        return redirect(url_for('admin.list_plan'))

    return render_template('admin/plans/plan.html',
                           form=form,
                           plan=plan,
                           title='Add Plan')


@admin.route('/plans/add/day', methods=['GET', 'POST'])
@login_required
def add_plan_day():
    """
    Add one plan
    """
    check_admin()

    form = PlanFormDay()
    if form.validate_on_submit():
        for leson in range(1,8):
            plan = EducationPlan(year=form.year.data,
                                 day=form.day.data,
                                 lessonNumber=leson,
                                 semester=form.semester.data)
            try:
                db.session.add(plan)
                db.session.commit()
                flash('You have successfully add the Plan.{}'.format(plan), category='message')
            except:
                flash('Such a Plan already exists.', category='error')

        return redirect(url_for('admin.list_plan'))

    return render_template('admin/plans/plan.html',
                           form=form,
                           title='Add Plan 1-7 lesson')