from flask import Blueprint
from flask import request
from flask import jsonify
from flask import session
from flask import redirect
from flask import url_for

import flask_login

from app.svc.membership import fake_driver as membership_driver
from . import forms

bp = Blueprint(__name__.split('.')[2], __name__)


@bp.route('sign-up', methods=['POST'])
def sign_up():
    form = forms.SignUpForm()
    if not form.validate_on_submit():
        return 'sign up error 1'
    user = membership_driver.create_user(
        form.username.data, form.email.data, form.password.data)
    if user:
        if not flask_login.login_user(user, remember=True):
            return 'sign in error 4'
        return redirect(url_for('site.index'))
    else:
        return 'sign up error 2 (already have an account)'


@bp.route('sign-in', methods=['POST'])
def sign_in():
    form = forms.SignInForm()
    if not form.validate_on_submit():
        return 'sign in error 1'
    user = membership_driver.get_user_by_email(form.email.data)
    if not user:
        return 'sign in error 2'
    if not membership_driver.verify_user(user.user_id, form.password.data):
        return 'sign in error 3'
    if not flask_login.login_user(user, remember=True):
        return 'sign in error 4'
    return redirect(url_for('site.index'))


@bp.route('sign-out', methods=["POST"])
def sign_out():
    form = forms.SignOutForm()
    if not form.validate_on_submit():
        return 'sign out error 1'
    flask_login.logout_user()
    return redirect(url_for('site.index'))
