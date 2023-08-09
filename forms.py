from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import Length,EqualTo,DataRequired

class RegisterForm(FlaskForm):
    name = StringField(label = 'Name',validators=[Length(min=2,max=30),DataRequired()])
    password1 = PasswordField(label = 'Password',validators=[Length(min=6),DataRequired()])
    password2 = PasswordField(label = 'Cofirm Password',validators=[EqualTo('password1'),DataRequired()])
    submit = SubmitField(label = 'Create Account!')

class LoginForm(FlaskForm):
    name = StringField(label='Name',validators=[DataRequired()])
    password = PasswordField(label='Password',validators=[DataRequired()])
    submit = SubmitField(label='Log In!')