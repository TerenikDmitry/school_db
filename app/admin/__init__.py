from flask import Blueprint, abort
from flask_login import current_user

admin = Blueprint('admin', __name__)


def check_admin():
    """
    Prevent non-admins from accessing the page
    """
    if not current_user.is_admin:
        abort(403)


from . import views_classrooms
from . import views_parents_info
from . import views_roles
from . import views_specialization
from . import views_students_class
from . import views_teachers_info
from . import views_users
from . import views_plan
from . import views_schedule
from . import views_classes
