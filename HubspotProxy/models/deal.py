from config.database import db
# from flask_mongoengine import Document 
from flask_mongoengine import BaseQuerySet


class Deal(db.Document):
    deal_id = db.StringField(required=True)
    dealname = db.StringField(max_length=50, required=True)
    dealstage = db.StringField(max_length=50, required=True)
    createdate = db.StringField(max_length=50, required=True)
    amount = db.IntField(required=True)

    meta = { 'collection': 'deals', 'queryset_class': BaseQuerySet}
