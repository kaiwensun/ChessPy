from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, StringField, validators
from wtforms.fields.html5 import EmailField
from app.shared import utils


class SignUpForm(FlaskForm):
    username = StringField(
        utils.gettext("User name"),
        [validators.DataRequired(utils.gettext("user name is required")),
         validators.Length(3, 32, utils.gettext(
             "user name must be between 3 and 32 charactors long"))],
        render_kw={"placeholder": utils.gettext("Your name")})
    email = EmailField(
        utils.gettext("Email"),
        [validators.DataRequired(utils.gettext("email is required")),
         validators.Email(utils.gettext("your email is requried"))],
        render_kw={"placeholder": utils.gettext("Your email address")})
    password = PasswordField(
        utils.gettext("Password"),
        [validators.Length(8, 32, utils.gettext(
            "password must be between 8 and 32 charactors long")),
         validators.DataRequired(utils.gettext("password is required"))])
    password_confirm = PasswordField(
        utils.gettext("Repeat password"),
        [validators.DataRequired(utils.gettext(
            "please confirm your password")),
         validators.EqualTo("password", message=utils.gettext(
             "password must match"))])


class SignInForm(FlaskForm):
    email = EmailField(
        utils.gettext("Email"),
        [validators.DataRequired(utils.gettext("email is required")),
         validators.Email(utils.gettext("your email is requried"))],
        render_kw={"placeholder": utils.gettext("Your email address")})
    password = PasswordField(
        utils.gettext("Password"),
        [validators.Length(8, 32, utils.gettext(
            "password incorrect")),
         validators.DataRequired(utils.gettext("password is required"))])
