from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, BooleanField, SubmitField
from wtforms.ext.dateutil.fields import DateTimeField, DateField
from wtforms.validators import Required


class RecordTimeForm(Form):
    input_date = DateField(u'Date', validators=[Required()])
    input_start = DateTimeField(u'Start', validators=[Required()])
    input_stop = DateTimeField(u'Stop')
    interruption = StringField(u'Interruption')
    delta = StringField(u'Delta')
    activity = StringField(u'Activity')
    comments = TextAreaField(u'Comments')
    complete = BooleanField(u'Complete')
    submit = SubmitField('Submit')
