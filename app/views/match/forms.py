from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, StringField, validators
from wtforms.fields.html5 import EmailField
from app.shared import utils


class CreateMatchForm(FlaskForm):
    join_token = StringField(
        utils.gettext("Join token"),
        [validators.Optional(),
         validators.Length(
            max=32,
            message=utils.gettext(
                "Join token must be no more than 32 letters long"))])


class JoinMatchForm(FlaskForm):
    join_token = StringField(
        utils.gettext("Join token"),
        [validators.DataRequired(utils.gettext("A join token is requried")),
         validators.Length(
            max=32,
            message=utils.gettext(
                "Join token must be no more than 32 letters long"))])
