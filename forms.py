from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.fields.simple import  FileField, EmailField
from wtforms.validators import DataRequired, Optional



class UploadPictureForm(FlaskForm):
    photo = FileField('Photo', validators=[FileRequired()])
    logo = FileField('Logo (Choose this or text)', validators=[Optional()])
    water_text = StringField('Water Mark Text (Choose this or Logo)', validators=[Optional()])
    name = StringField('File Name', validators=[DataRequired()])
    submit = SubmitField('Submit')

class ContactForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Submit')


