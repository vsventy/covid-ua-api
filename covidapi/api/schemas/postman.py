from covidapi.extensions import db, ma
from covidapi.models.postman import PostmanNotification


class NotificationSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = PostmanNotification
        sqla_session = db.session
        load_instance = True
        exclude = (
            "api_token",
        )
