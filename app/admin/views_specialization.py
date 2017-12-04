from flask import flash, redirect, render_template, url_for
from flask_login import login_required

from . import admin, check_admin
from .. import db
from forms import SpecializationForm
from ..models import Specialization, RoomSpecialization, Subject


@admin.route('/class_specializations')
@login_required
def list_class_specializations():
    """
    Show the list of specializations of classes
    """
    check_admin()

    specializations = Specialization.query.order_by(Specialization.name).all()
    return render_template('admin/class_specializations/class_specializations.html',
                           specializations=specializations)


@admin.route('/class_specializations/add', methods=['GET', 'POST'])
@login_required
def add_class_specialization():
    """
    Add class specialization
    """
    check_admin()

    form = SpecializationForm()
    if form.validate_on_submit():
        specialization = Specialization(name=form.name.data)

        try:
            db.session.add(specialization)
            db.session.commit()
            flash('You have successfully added a new specialization.')
        except:
            flash('Error: specialization name already exists.')

        # redirect to the list of specializations of classes PAGE
        return redirect(url_for('admin.list_class_specializations'))

    return render_template('admin/class_specializations/class_specialization.html',
                           form=form,
                           title='Add Class Specialization')


@admin.route('/class_specializations/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_class_specialization(id):
    """
    Delete class specialization
    """
    check_admin()

    specialization = Specialization.query.get_or_404(id)
    db.session.delete(specialization)
    db.session.commit()
    flash('You have successfully deleted the specialization.')

    # redirect to the list of specializations of classes PAGE
    return redirect(url_for('admin.list_class_specializations'))


@admin.route('/class_specializations/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_class_specialization(id):
    """
    Edit class specialization
    """
    check_admin()

    specialization = Specialization.query.get_or_404(id)
    form = SpecializationForm(obj=specialization)
    if form.validate_on_submit():
        specialization.name = form.name.data
        db.session.add(specialization)
        db.session.commit()
        flash('You have successfully edited the specialization.')

        # redirect to the list of specializations of classes PAGE
        return redirect(url_for('admin.list_class_specializations'))

    form.name.data = specialization.name
    return render_template('admin/class_specializations/class_specialization.html',
                           spec_name=specialization.name,
                           form=form,
                           title="Edit Class Specialization")


@admin.route('/room_specializations')
@login_required
def list_room_specializations():
    """
    Show the list of specializations of classroom
    """
    check_admin()

    room_specializations = RoomSpecialization.query.order_by(RoomSpecialization.name).all()
    return render_template('admin/room_specializations/room_specializations.html',
                           room_specializations=room_specializations, )


@admin.route('/room_specializations/add', methods=['GET', 'POST'])
@login_required
def add_room_specialization():
    """
    Add classroom specialization
    """
    check_admin()

    form = SpecializationForm()
    if form.validate_on_submit():
        room_specialization = RoomSpecialization(name=form.name.data)

        try:
            db.session.add(room_specialization)
            db.session.commit()
            flash('You have successfully added a new classroom specialization.')
        except:
            flash('Error: class specialization name already exists.')

        # redirect to the list of specializations of classroom PAGE
        return redirect(url_for('admin.list_room_specializations'))

    return render_template('admin/room_specializations/room_specialization.html',
                           form=form,
                           title='Add Room Specialization')


@admin.route('/room_specializations/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_room_specialization(id):
    """
    Delete classroom specialization
    """
    check_admin()

    room_specializations = RoomSpecialization.query.get_or_404(id)
    db.session.delete(room_specializations)
    db.session.commit()
    flash('You have successfully deleted the classroom specialization.')

    # redirect to the list of specializations of classroom PAGE
    return redirect(url_for('admin.list_room_specializations'))


@admin.route('/room_specializations/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_room_specialization(id):
    """
    Edit classroom specialization
    """
    check_admin()

    room_specialization = RoomSpecialization.query.get_or_404(id)
    form = SpecializationForm(obj=room_specialization)
    if form.validate_on_submit():
        room_specialization.name = form.name.data
        db.session.add(room_specialization)
        db.session.commit()
        flash('You have successfully edited the room specialization.')

        # redirect to the list of specializations of classroom PAGE
        return redirect(url_for('admin.list_room_specializations'))

    form.name.data = room_specialization.name
    return render_template('admin/room_specializations/room_specialization.html',
                           spec_name=room_specialization.name,
                           form=form,
                           title="Edit Room Specialization")


@admin.route('/subjects')
@login_required
def list_subjects():
    """"
    Show the list of subjects
    """
    check_admin()

    subjects = Subject.query.order_by(Subject.name).all()
    return render_template('admin/subjects/list.html',
                           subjects=subjects)


@admin.route('/subjects/add', methods=['GET', 'POST'])
@login_required
def add_subject():
    """
    Add subject
    """
    check_admin()

    form = SpecializationForm()
    if form.validate_on_submit():
        subject = Subject(name=form.name.data)

        try:
            db.session.add(subject)
            db.session.commit()
            flash('You have successfully added a new subject.')
        except:
            flash('Error: subject name already exists.')

        # redirect to the list of subjects PAGE
        return redirect(url_for('admin.list_subjects'))

    return render_template('admin/subjects/edit.html',
                           form=form,
                           title='Add Subject')


@admin.route('/subjects/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_subject(id):
    """
    Edit subject
    """
    check_admin()

    subject = Subject.query.get_or_404(id)
    form = SpecializationForm(obj=subject)
    if form.validate_on_submit():
        subject.name = form.name.data
        db.session.add(subject)
        db.session.commit()
        flash('You have successfully edited the subject.')

        # redirect to the list of subjects PAGE
        return redirect(url_for('admin.list_subjects'))

    form.name.data = subject.name
    return render_template('admin/subjects/edit.html',
                           subject_name=subject.name,
                           form=form,
                           title="Edit Subject")


@admin.route('/subjects/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_subject(id):
    """
    Delete subject
    """
    check_admin()

    subject = Subject.query.get_or_404(id)
    db.session.delete(subject)
    db.session.commit()
    flash('You have successfully deleted the subject.')

    # redirect to the list of subjects PAGE
    return redirect(url_for('admin.list_subjects'))