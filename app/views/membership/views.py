from flask import Blueprint
from flask import request

from app.svc.membership import fake_driver as membership_driver
from . import forms

bp = Blueprint(__name__.split('.')[2], __name__)


@bp.route('sign-up', methods=['POST'])
def sign_up():
    form = forms.SignUpForm(request.form)
    # TODO: implement post sign in page
    if not form.validate():
        return 'error 1'
    if membership_driver.create_user(
            form.username.data, form.email.data, form.password.data):
        return 'OK'
    else:
        return 'error 2'
