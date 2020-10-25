from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField, TextAreaField
from wtforms.validators import InputRequired

    
# form for new post
class PostForm(FlaskForm):
                            #label
    title = StringField('Title', validators=[InputRequired('Title is required')])
    content = TextAreaField('Content', validators=[InputRequired('Post is blank')])
    submit = SubmitField('Post')
    
    
