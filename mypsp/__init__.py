import os
from flask import Flask, redirect, url_for, render_template
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, BooleanField, SubmitField
from wtforms.ext.dateutil.fields import DateTimeField, DateField
from wtforms.validators import Required


basedir = os.path.abspath(os.path.dirname(__file__))


app = Flask(__name__)
app.debug = True
app.secret_key = "WHAT DO you mean"
app.config['SECRET_KEY'] = 'Thear cean be only won'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'data.sqlite')
# enable automatic commits of database changes at the end of each request
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

manager = Manager(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class TimeRecord(db.Model):
    __tablename__ = 'records'
    id = db.Column(db.Integer, primary_key=True)
    record_date = db.Column(db.DateTime)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    interruption = db.Column(db.Integer)  # in minutes
    delta_time = db.Column(db.Integer)  # in minutes
    activity = db.Column(db.String(128))
    comments = db.Column(db.String(256))
    complete = db.Column(db.Boolean, default=False)
    units = db.Column(db.Integer)

    def __repr__(self):
        return '<Record %r - activity: %r>' % (self.id, self.activity)


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


def make_shell_context():
    return dict(app=app, db=db, TimeRecord=TimeRecord)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command("db", MigrateCommand)


@app.route("/", methods=['GET', 'POST'])
def index():
    records = TimeRecord.query.all()
    form = RecordTimeForm()
    if form.validate_on_submit():
        record = TimeRecord(record_date=form.input_date.data,
                            start_date=form.input_start.data,
                            end_date=form.input_stop.data,
                            interruption=form.interruption.data,
                            delta_time=form.delta.data,
                            activity=form.activity.data,
                            comments=form.comments.data,
                            complete=form.complete.data)
        db.session.add(record)
        return redirect(url_for('.index'))
    print form.errors
    return render_template('index.html', form=form, records=records)


if __name__ == "__main__":
    manager.run()
