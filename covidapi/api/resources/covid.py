from datetime import date, datetime

from flask import request

from flask_restful import Resource
from sqlalchemy import func, desc

from covidapi.api.schemas import CovidItemSchema
from covidapi.commons.pagination import paginate
from covidapi.extensions import db
from covidapi.models.covid import CovidItem


class CovidResource(Resource):
    """Single object resource

    ---
    get:
      tags:
        - api
      parameters:
        - in: query
          name: day
          schema:
            type: string
            format: date
            example: "2020-05-01"
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  item: CovidItemSchema
        404:
          description: covid_item does not exists
    """
    def get(self):
        schema = CovidItemSchema()

        if 'day' in request.args:
            dt = datetime.strptime(request.args['day'], '%Y-%m-%d').date()
        else:
            dt = date.today()

        covid_item = (
            db.session.query(CovidItem)
            .filter(func.DATE(CovidItem.updated_at) == dt)
            .order_by(desc(CovidItem.updated_at))
            .first()
        )
        return {"item": schema.dump(covid_item)}


class CovidItemList(Resource):
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
                          $ref: '#/components/schemas/CovidItemSchema'
    """
    def get(self):
        schema = CovidItemSchema(many=True)
        query = CovidItem.query
        return paginate(query, schema)