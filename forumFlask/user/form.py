from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import BooleanField, StringField, PasswordField, validators, SubmitField
from wtforms.validators import InputRequired, Email, Length, EqualTo, ValidationError
from forumFlask.models import User


class RegistrationForm(FlaskForm):
                            #label
    username = StringField('Username', validators=[InputRequired('Must enter usrname'), Length(min=4, max=25)])
    email = StringField('Email Address', validators=[InputRequired(), Length(min=6, max=35), Email()])
    password = PasswordField('New Password', validators=[InputRequired()])
    confirm = PasswordField('Repeat Password', validators=[
        InputRequired(),
        EqualTo('password', message='Passwords mismatch')])
    submit = SubmitField('Sign Up')
    
    #check if email already registered
    def validate_email(self, email):
        emailDb = User.query.filter_by(email=email.data).first()
        if emailDb:
            raise ValidationError('Email already registered')
    
    
class LoginForm(FlaskForm):
    
    email = StringField('Email Address', validators=[InputRequired(), Length(min=6, max=35), Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign In')
    
    
# form for update account page, username, profile pic
class AccountForm(FlaskForm):
                            #label
    username = StringField('Username', validators=[InputRequired('Must enter usrname'), Length(min=4, max=25)])
    img = FileField('Profile pic', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')
    
    
    
# form for reset password request
class ResetPassRequestForm(FlaskForm):
    email = StringField('Email Address', validators=[InputRequired(), Length(min=6, max=35), Email()])
    submit = SubmitField('Reset Password')
    
    #check if email already registered
    def validate_email(self, email):
        emailDb = User.query.filter_by(email=email.data).first()
        if not emailDb:
            raise ValidationError('Email not registered')


# reset pw
class ResetPassForm(FlaskForm):
    password = PasswordField('New Password', validators=[InputRequired()])
    confirm = PasswordField('Repeat Password', validators=[
        InputRequired(),
        EqualTo('password', message='Passwords mismatch')])
    submit = SubmitField('Save')