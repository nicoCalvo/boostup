from config.database import db


class Deal(db.Document):
    deal_id = db.StringField(required=True)
    name = db.StringField(max_length=50, required=True)
    stage = db.StringField(max_length=50, required=True)
    date = db.StringField(max_length=50, required=True)
    amount = db.IntField(required=True)

