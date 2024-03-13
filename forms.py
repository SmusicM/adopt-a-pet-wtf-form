from flask_wtf import FlaskForm
from wtforms import StringField, FloatField,BooleanField,IntegerField,RadioField,SelectField
from wtforms.validators import InputRequired, Optional, Email,NumberRange,URL

class PetForm(FlaskForm):
    name = StringField("Pet Name",validators=[InputRequired(message="Pet Name is required")])
    species = SelectField("Species",choices=[("dog","Dog"),("cat","Cat"),("porcupine","Porcupine")],validators=[InputRequired(message="must select a species")])
    photo_url = StringField("Photo URL",validators=[Optional(),URL(message="must be url")],default = "https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png")
    age = IntegerField("Age",validators=[Optional(),NumberRange(min=0,max=30,message="age must e between 0 and 30")])
    notes = StringField("Notes")
    available = BooleanField("Available",validators=[Optional()])