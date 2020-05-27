from flask import Blueprint, current_app, jsonify
from flask_restful import Api
from marshmallow import ValidationError

from covidapi.extensions import apispec
from covidapi.api.resources import (
    CovidItemList,
    CovidResource,
    NotificationList,
    NotificationResource,
    UserList,
    UserResource,
)
from covidapi.api.schemas import (
    CovidItemSchema,
    NotificationSchema,
    UserSchema,
)

blueprint = Blueprint("api", __name__, url_prefix="/api/v1")
api = Api(blueprint)


api.add_resource(CovidResource, "/covid", endpoint="covid_by_date")
api.add_resource(CovidItemList, "/covid/list", endpoint="covid_items")
api.add_resource(NotificationResource, "/postman/<int:id>", endpoint="notification_by_id")
api.add_resource(NotificationList, "/postman/list", endpoint="notifications")
api.add_resource(UserResource, "/users/<int:user_id>", endpoint="user_by_id")
api.add_resource(UserList, "/users", endpoint="users")


@blueprint.before_app_first_request
def register_views():
    # apispec.spec.components.schema("UserSchema", schema=UserSchema)
    # apispec.spec.path(view=UserResource, app=current_app)
    # apispec.spec.path(view=UserList, app=current_app)

    apispec.spec.components.schema("CovidItemSchema", schema=CovidItemSchema)
    apispec.spec.path(view=CovidResource, app=current_app)
    apispec.spec.path(view=CovidItemList, app=current_app)

    apispec.spec.components.schema("NotificationSchema", schema=NotificationSchema)
    apispec.spec.path(view=NotificationResource, app=current_app)
    apispec.spec.path(view=NotificationList, app=current_app)


@blueprint.errorhandler(ValidationError)
def handle_marshmallow_error(e):
    """Return json error for marshmallow validation errors.

    This will avoid having to try/catch ValidationErrors in all endpoints, returning
    correct JSON response with associated HTTP 400 Status (https://tools.ietf.org/html/rfc7231#section-6.5.1)
    """
    return jsonify(e.messages), 400
