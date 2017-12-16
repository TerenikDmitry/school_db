from . import admin, check_admin
from .. import db

from flask import render_template, flash, redirect, url_for
from flask_login import login_required

from .forms import RegistrationForm, UserEditForm

from ..models import User


@admin.route('/users/<int:pagin>')
@login_required
def list_users(pagin):
    """
    List all users
    """
    check_admin()

    users = User.query.order_by(User.role_id,User.last_name).paginate(page=pagin, per_page=10)
    return render_template('admin/users/users.html',
                           users=users)


@admin.route('/users/add', methods=['GET', 'POST'])
@login_required
def add_user():
    """
    Add a user
    """
    check_admin()

    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            user = User(email=form.email.data,
                        date_of_birth=form.date_of_birth.data,
                        first_name=form.first_name.data,
                        last_name=form.last_name.data,
                        middle_name=form.middle_name.data,
                        password=form.password.data,
                        role_id=form.role.data.id,
                        telephone=form.telephone.data,
                        is_man=form.is_man.data)
            db.session.add(user)
            db.session.commit()
            flash('You have successfully added a user.',category='message')
        except:
            flash('Error in adding user.', category='error')

        # redirect to the user list PAGE
        return redirect(url_for('admin.list_users', pagin=1))

    return render_template('admin/users/user.html',
                           form=form)


@admin.route('/users/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_user(id):
    """
    Delete a user
    """
    check_admin()

    try:
        user = User.query.get_or_404(id)
        db.session.delete(user)
        db.session.commit()
        flash('You have successfully deleted the user.',category='message')
    except:
        flash('Error in deleting user.', category='error')

    # redirect to the user list PAGE
    return redirect(url_for('admin.list_users', pagin=1))


@admin.route('/users/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_user(id):
    """
    Change user information
    """
    check_admin()

    user = User.query.get_or_404(id)

    form = UserEditForm(obj=user)
    if form.validate_on_submit():
        try:
            user.date_of_birth = form.date_of_birth.data
            user.first_name = form.first_name.data
            user.last_name = form.last_name.data
            user.middle_name = form.middle_name.data
            user.email = form.email.data
            user.telephone = form.telephone.data
            user.is_man = form.is_man.data
            db.session.add(user)
            db.session.commit()
            flash('You have successfully changed the user information.',category='message')
        except:
            flash('Error in changing user information.', category='error')

        # redirect to the user list PAGE
        return redirect(url_for('admin.list_users', pagin=1))

    return render_template('admin/users/user.html',
                           user=user,
                           form=form)