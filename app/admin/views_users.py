from . import admin, check_admin
from .. import db

from flask import render_template, flash, redirect, url_for
from flask_login import login_required

from forms import RegistrationForm, UserEditForm

from ..models import Role, User


@admin.route('/users')
@login_required
def list_users():
    """
    List all users
    """
    check_admin()

    users = User.query.all()
    return render_template('admin/users/users.html',
                           users=users,
                           title='Users')


@admin.route('/users/add', methods=['GET', 'POST'])
@login_required
def add_user():
    """
    Add a user
    """
    check_admin()

    add_user = True
    user = User()
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    middle_name=form.middle_name.data,
                    password=form.password.data,
                    role_id=form.role.data.id,
                    tel=form.tell.data)

        db.session.add(user)
        db.session.commit()
        flash('You have successfully add user.')

        # redirect to the user list PAGE
        return redirect(url_for('admin.list_users'))

    return render_template('admin/users/user.html',
                           user=user,
                           form=form,
                           title='Add User',
                           add_user=add_user)


@admin.route('/users/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_user(id):
    """
    Delete a user
    """
    check_admin()

    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    flash('You have successfully deleted the user.')

    # redirect to the user list PAGE
    return redirect(url_for('admin.list_users'))


@admin.route('/users/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_user(id):
    """
    Change user information
    """
    check_admin()

    add_user = False

    user = User.query.get_or_404(id)

    form = UserEditForm(obj=user)
    if form.validate_on_submit():
        user.role_id = form.role.data.id
        user.username = form.username.data
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.middle_name = form.middle_name.data
        user.email = form.email.data
        user.tel = form.tell.data
        db.session.add(user)
        db.session.commit()
        flash('You have successfully assigned a role.')

        # redirect to the user list PAGE
        return redirect(url_for('admin.list_users'))

    form.username.data = user.username
    form.first_name.data = user.first_name
    form.last_name.data = user.last_name
    form.middle_name.data = user.middle_name
    form.email.data = user.email
    form.tell.data = user.tel
    form.role.data = Role.query.get_or_404(user.role_id)

    return render_template('admin/users/user.html',
                           user=user,
                           form=form,
                           title='Edit User',
                           add_user=add_user)