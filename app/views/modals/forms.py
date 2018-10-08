from wtforms import Form, StringField, PasswordField, validators, StringField
from app.shared import utils


class SignUpForm(Form):
    username = StringField(
        utils.gettext("User name"),
        [validators.DataRequired(utils.gettext("user name is required")),
         validators.Length(3, 32, utils.gettext(
            "user name must be between 3 and 32 charactors long"))],
        render_kw={"placeholder": utils.gettext("Your name")})
    email = StringField(
        utils.gettext("Email"),
        [validators.InputRequired(utils.gettext("email is required")),
         validators.Email(utils.gettext("your email is requried"))],
        render_kw={"placeholder": utils.gettext("Your email address")})
    password = PasswordField(
        utils.gettext("Password"),
        [validators.Length(8, 32, utils.gettext(
            "password must be between 8 and 32 charactors long")),
         validators.InputRequired(utils.gettext("password is required"))])
    password_confirm = PasswordField(
        utils.gettext("Repeat password"),
        [validators.InputRequired(utils.gettext(
            "please confirm your password")),
         validators.EqualTo("password", message=utils.gettext(
            "password must match"))])
