from flask import Blueprint, render_template
from app.views.match import forms as match_forms
from app.views.membership import forms as membership_forms

bp = Blueprint(__name__.split('.')[2], __name__)


@bp.route('/sign-in-modal')
def sign_in_modal():
    return render_template('modals/authentication.html',
                           form=membership_forms.SignInForm(),
                           form_id='sign-in-form',
                           action_endpoint='membership.sign_in',
                           field_names=['email', 'password'],
                           button_text='Sign in')


@bp.route('/sign-up-modal')
def sign_up_modal():
    return render_template('modals/authentication.html',
                           form=membership_forms.SignUpForm(),
                           form_id='sign-up-form',
                           action_endpoint='membership.sign_up',
                           field_names=[
                               'username', 'email', 'password',
                               'password_confirm'],
                           button_text='Sign up')


@bp.route('/sign-out-modal')
def sign_out_modal():
    return render_template('modals/authentication.html',
                           message="See you next time!",
                           form=membership_forms.SignOutForm(),
                           form_id='sign-up-form',
                           action_endpoint='membership.sign_out',
                           field_names=[],
                           button_text='Sign out')


@bp.route('join_private_match_modal')
def join_private_game_modal():
    form = match_forms.JoinPrivateMatchForm()
    return render_template('modals/authentication.html',
                           form=form,
                           form_id='join-private-match-form',
                           action_endpoint='match.join_private_match',
                           field_names=['join_token'],
                           button_text="Join game")
