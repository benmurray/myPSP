import os
from flask import Flask, render_template
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.wtf import Form
from wtforms import DateField, DateTimeField, StringField, TextAreaField, \
    RadioField, SubmitField
from wtforms.validators import Required


basedir = os.path.abspath(os.path.dirname(__file__))


app = Flask(__name__)
app.debug = True
app.secret_key = "WHAT DO you mean"
app.config['SECRET_KEY'] = 'Thear cean be only won'
app.config['BOOTSTRAP_SERVE_LOCAL'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'data.sqlite')
# enable automatic commits of database changes at the end of each request
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class TimeRecord(db.Model):
    __tablename__ = 'records'
    id = db.Column(db.Integer, primary_key=True)
    record_date = db.Column(db.Date)
    start_date = db.Column(db.Time)
    end_date = db.Column(db.Time)
    interupption = db.Column(db.Integer)  # in minutes
    delta_time = db.Column(db.Integer)  # in minutes
    activity = db.Column(db.String(128))
    comments = db.Column(db.String(256))
    complete = db.Column(db.Boolean, default=False)
    units = db.Column(db.Integer)

    def __repr__(self):
        return '<Record %r - activity: %r>' % (self.id, self.activity)


class RecordTimeForm(Form):
    date = DateField(u'Date', validators=[Required()])
    start = DateTimeField(u'Start', validators=[Required()])
    stop = DateTimeField(u'Stop')
    interruption = StringField(u'Interruption')
    delta = StringField(u'Delta')
    activity = StringField(u'Activity')
    comments = TextAreaField(u'Comments')
    complete = RadioField(u'Complete', choices=[(False, 'N/A'), (True, 'Yes'),
                                                (False, 'No')])
    submit = SubmitField('Submit')


def make_shell_context():
    return dict(app=app)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command("db", MigrateCommand)


@app.route("/", methods=['GET', 'POST'])
def index():
    activity = ""
    form = RecordTimeForm()
    if form.validate_on_submit():
        activity = form.activity.data
    return render_template('index.html', form=form, activity=activity)


if __name__ == "__main__":
    manager.run()
