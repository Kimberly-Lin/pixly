from flask_wtf import FlaskForm
from wtforms import StringField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import length

class ImageForm(FlaskForm):
    """Form for uploading images. Validates for file types of """

    image = FileField('Image', 
        validators=[FileRequired(), 
            FileAllowed(['png','jpg', 'jpeg'], '.png, .jpg or .jpeg only!')])
    title = StringField('Title', validators=[length(max=100)])