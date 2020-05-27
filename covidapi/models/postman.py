import enum

from covidapi.extensions import db


class ServiceType(enum.IntEnum):
    EMAIL = 0
    SMS = 1
    TELEGRAM = 2
    VIBER = 3


class NotifyType(enum.IntEnum):
    TEXT = 0
    TEMPLATE = 1


class PostmanNotification(db.Model):
    """Postman notification representation
    """

    __table_name__ = 'postman_notification'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    api_token = db.Column(db.String(100), nullable=False, unique=True)
    service_type = db.Column(db.Enum(ServiceType), nullable=False)
    notify_type = db.Column(db.Enum(NotifyType), nullable=False)
    template_key = db.Column(db.String(100), nullable=True)
    message_text = db.Column(db.String(1000), nullable=True)
    is_active = db.Column(db.Boolean, default=True)

    user = db.relationship("User", lazy="joined")

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "api_token": self.api_token,
            "service_type": self.service_type,
            "notify_type": self.notify_type,
            "template_key": self.template_key,
            "message_text": self.message_text,
            "email": self.user.email,
            "phone": self.user.phone,
            "is_active": self.is_active,
        }

    def __repr__(self):
        return '<PostmanNotification {}>'.format(self.id)
