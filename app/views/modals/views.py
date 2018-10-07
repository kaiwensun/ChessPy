from flask import Blueprint, render_template
from . import forms

bp = Blueprint(__name__.split('.')[2], __name__)

@bp.route('/sign-in-modal')
def sign_in_modal():
    return render_template('modals/sign_in_modal.html', form=forms.SignUpForm())

@bp.route('/sign-up-modal')
def sign_up_modal():
    return render_template('modals/sign_up_modal.html', form=forms.SignUpForm())
