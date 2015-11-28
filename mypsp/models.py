from . import db


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
