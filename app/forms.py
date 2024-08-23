# forms.py

from flask_wtf import FlaskForm
from wtforms import SelectMultipleField, SubmitField
from wtforms.validators import DataRequired

class TechStackForm(FlaskForm):
    tech_stack = SelectMultipleField('Select Technologies', validators=[DataRequired()])
    submit = SubmitField('Analyze')