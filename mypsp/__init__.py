from flask import Flask, flash, render_template, request
from flask.ext.script import Manager
from flask.ext.wtf import Form
from wtforms import DateField, DateTimeField, StringField, TextAreaField, \
    RadioField, SubmitField
from wtforms.validators import Required


app = Flask(__name__)
manager = Manager(app)


class RecordTimeForm(Form):
    date = DateField(u'Date', validators=[Required()])
    start = DateTimeField(u'Start', validators=[Required()])
    stop = DateTimeField(u'Stop')
    interruption = StringField(u'Interruption')
    delta = StringField(u'Delta')
    activity = StringField(u'Activity')
    comments = TextAreaField(u'Comments')
    complete = RadioField(u'Complete', choices=['N/A', 'Yes', 'No'])
    submit = SubmitField('Submit')


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # flash("This is me testing")
        flash(request.form['inputActivity'])
    return render_template('index.html')


if __name__ == "__main__":
    app.debug = True
    app.secret_key = "WHAT DO you mean"
    app.config['SECRET_KEY'] = 'Thear cean be only won'
    manager.run()
