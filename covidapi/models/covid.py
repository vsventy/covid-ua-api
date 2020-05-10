from covidapi.extensions import db


class CovidItem(db.Model):
    """Item representation of Covid-19
    """

    __tablename__ = 'covid_items'

    id = db.Column(db.Integer, primary_key=True)
    confirmed = db.Column(db.Integer, nullable=False)
    active = db.Column(db.Integer, nullable=False)
    recovered = db.Column(db.Integer, nullable=False)
    deaths = db.Column(db.Integer, nullable=False)
    total_confirmed = db.Column(db.Integer, nullable=False)
    total_active = db.Column(db.Integer, nullable=False)
    total_recovered = db.Column(db.Integer, nullable=False)
    total_deaths = db.Column(db.Integer, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def to_dict(self):
        return {
            "total": {
                "confirmed": self.total_confirmed,
                "active": self.total_active,
                "recovered": self.total_recovered,
                "deaths": self.total_deaths
            },
            "per_day": {
                "confirmed": self.confirmed,
                "active": self.active,
                "recovered": self.recovered,
                "deaths": self.deaths
            },
            "updated_at": self.updated_at,
        }

    def __repr__(self):
        return '<CovidItem {} by {}>'.format(self.id, self.updated_at)