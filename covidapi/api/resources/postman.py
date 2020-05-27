from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required

from covidapi.api.schemas import NotificationSchema
from covidapi.commons.pagination import paginate
from covidapi.extensions import db
from covidapi.models.postman import PostmanNotification


class NotificationResource(Resource):
    """Single object resource

    ---
    get:
      tags:
        - api
      parameters:
        - in: path
          name: id
          schema:
            type: integer
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  notification: NotificationSchema
        404:
          description: notification does not exists
    put:
      tags:
        - api
      parameters:
        - in: path
          name: id
          schema:
            type: integer
      requestBody:
        content:
          application/json:
            schema:
              NotificationSchema
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    type: string
                    example: notification updated
                  notification: NotificationSchema
        404:
          description: notification does not exists
    delete:
      tags:
        - api
      parameters:
        - in: path
          name: id
          schema:
            type: integer
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    type: string
                    example: notification deleted
        404:
          description: notification does not exists
    """

    method_decorators = [jwt_required]

    def get(self, id):
        schema = NotificationSchema()
        notification = PostmanNotification.query.get_or_404(id)
        return {"notification": schema.dump(notification)}

    def put(self, id):
        schema = NotificationSchema(partial=True)
        notification = PostmanNotification.query.get_or_404(id)
        notification = schema.load(request.json, instance=notification)

        db.session.commit()

        return {
            "msg": "notification updated",
            "notification": schema.dump(notification)
        }

    def delete(self, id):
        notification = PostmanNotification.query.get_or_404(id)
        db.session.delete(notification)
        db.session.commit()

        return {"msg": "notification deleted"}


class NotificationList(Resource):
    """Creation and get_all

    ---
    get:
      tags:
        - api
      responses:
        200:
          content:
            application/json:
              schema:
                allOf:
                  - $ref: '#/components/schemas/PaginatedResult'
                  - type: object
                    properties:
                      results:
                        type: array
                        items:
                          $ref: '#/components/schemas/NotificationSchema'
    post:
      tags:
        - api
      requestBody:
        content:
          application/json:
            schema:
              NotificationSchema
      responses:
        201:
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    type: string
                    example: notification created
                  notification: NotificationSchema
    """

    method_decorators = [jwt_required]

    def get(self):
        schema = NotificationSchema(many=True)
        query = PostmanNotification.query
        return paginate(query, schema)

    def post(self):
        schema = NotificationSchema()
        notification = schema.load(request.json)

        db.session.add(notification)
        db.session.commit()

        return {
            "msg": "notification created",
            "notification": schema.dump(notification)
        }, 201
