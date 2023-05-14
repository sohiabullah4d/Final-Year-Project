
from flask_wtf import FlaskForm

from wtforms import StringField, SubmitField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import DataRequired




class AddArticlesManuallyForm(FlaskForm):
    Papertitle = StringField('Paper title:',validators=[DataRequired()])
    Abstract = TextAreaField('Abstract:',validators=[DataRequired()])
    Keywords = StringField('Keywords:',validators=[DataRequired()])
    submit = SubmitField('Recommend')
    

class SearchForm(FlaskForm):
    Search = StringField('',validators=[DataRequired()])
    submit = SubmitField('Recommend')