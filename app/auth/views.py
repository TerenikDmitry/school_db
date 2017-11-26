from flask import flash, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user

from . import auth
from forms import LoginForm
from ..models import User

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():

        # check whether user exists in the database and whether
        # the password entered matches the password in the database
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)

            # redirect to the appropriate page
            if user.is_admin:
                return redirect(url_for('home.admin_dashboard'))
            elif user.role_id == 3:
                return redirect(url_for('home.parent_dashboard', id=user.id))
            elif user.role_id == 2:
                return redirect(url_for('home.student_dashboard', id=user.id))
            elif user.role_id == 1:
                return redirect(url_for('home.teacher_dashboard', id=user.id))
            else:
                return redirect(url_for('home.dashboard'))

        # when login details are incorrect
        else:
            flash("Invalid email or password.")

    return render_template('auth/login.html', form=form, title='Login')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have successfully been logged out.')

    # redirect to the login page
    return redirect(url_for('auth.login'))