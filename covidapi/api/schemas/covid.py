from covidapi.extensions import ma, db
from covidapi.models.covid import CovidItem


class CovidItemSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = CovidItem
        sqla_session = db.session
        load_instance = True
        exclude = (
            "id",
            "created_at",
        )
