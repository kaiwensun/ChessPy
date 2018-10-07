from wtforms import Form, StringField, PasswordField, validators, StringField

class SignUpForm(Form):
    username = StringField(
        "User name",
        [validators.DataRequired("user name is required"),
         validators.Length(3, 32, "user name must be between 3 and 32 charactors long")],
         render_kw={"placeholder": "Your name"})
    email = StringField(
        "Email",
        [validators.InputRequired("email is required"),
         validators.Email("your email is requried")],
         render_kw={"placeholder": "Your email address"})
    password = PasswordField(
        "Password",
        [validators.Length(8, 32, "password must be between 8 and 32 charactors long"),
         validators.InputRequired("password is required")])
    password_confirm = PasswordField(
        "Repeat password",
        [validators.InputRequired("please confirm your password"),
         validators.EqualTo("password", message="password must match")])
