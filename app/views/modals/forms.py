from wtforms import Form, StringField, PasswordField, validators, StringField
from flask_babel import lazy_gettext

class SignUpForm(Form):
    username = StringField(
        lazy_gettext("User name"),
        [validators.DataRequired(lazy_gettext("user name is required")),
         validators.Length(3, 32, lazy_gettext("user name must be between 3 and 32 charactors long"))],
         render_kw={"placeholder": lazy_gettext("Your name")})
    email = StringField(
        lazy_gettext("Email"),
        [validators.InputRequired(lazy_gettext("email is required")),
         validators.Email(lazy_gettext("your email is requried"))],
         render_kw={"placeholder": lazy_gettext("Your email address")})
    password = PasswordField(
        lazy_gettext("Password"),
        [validators.Length(8, 32, lazy_gettext("password must be between 8 and 32 charactors long")),
         validators.InputRequired(lazy_gettext("password is required"))])
    password_confirm = PasswordField(
        lazy_gettext("Repeat password"),
        [validators.InputRequired(lazy_gettext("please confirm your password")),
         validators.EqualTo("password", message=lazy_gettext("password must match"))])
