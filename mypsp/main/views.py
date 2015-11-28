from flask import render_template, url_for, redirect
from . import main
from .forms import RecordTimeForm
from .. import db
from ..models import TimeRecord


@main.route("/", methods=['GET', 'POST'])
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
