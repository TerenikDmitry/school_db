from . import admin, check_admin
from .. import db

from flask import render_template, flash, redirect, url_for
from flask_login import login_required

from .forms import RoleForm

from ..models import Role

@admin.route('/roles')
@login_required
def list_roles():
    """
    Show roles
    """
    check_admin()

    roles = Role.query.order_by(Role.name).all()

    return render_template('admin/roles/roles.html',
                           roles=roles)


@admin.route('/roles/add', methods=['GET', 'POST'])
@login_required
def add_role():
    """
    Add a role
    """
    check_admin()

    form = RoleForm()
    if form.validate_on_submit():
        role = Role(name=form.name.data,
                    description=form.description.data)

        try:
            # add role to the database
            db.session.add(role)
            db.session.commit()
            flash('You have successfully added a new Role.',category='message')
        except:
            flash('Error: Role name already exists.',category='error')

        # redirect to the list roles PAGE
        return redirect(url_for('admin.list_roles'))

    return render_template('admin/roles/role.html',
                           form=form,
                           title='Add Role')


@admin.route('/roles/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_role(id):
    """
    Edit a role
    """
    check_admin()

    role = Role.query.get_or_404(id)
    form = RoleForm(obj=role)
    if form.validate_on_submit():
        try:
            role.name = form.name.data
            role.description = form.description.data
            db.session.add(role)
            db.session.commit()
            flash('You have successfully edited the Role neme.',category='message')
        except:
            flash('Error in changing Roles name.', category='error')

        # redirect to the list roles PAGE
        return redirect(url_for('admin.list_roles'))

    return render_template('admin/roles/role.html',
                           form=form,
                           role_name=role.name,
                           title="Edit Role")


@admin.route('/roles/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def delete_role(id):
    """
    Delete a role
    """
    check_admin()

    role = Role.query.get_or_404(id)
    try:
        db.session.delete(role)
        db.session.commit()
        flash('You have successfully deleted the Role.',category='message')
    except:
        flash('Error in removing Roles.', category='error')

    return redirect(url_for('admin.list_roles'))