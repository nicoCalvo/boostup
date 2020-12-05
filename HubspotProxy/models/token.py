import time

from config.database import db



class Token(db.Document):
    refresh_token = db.StringField(max_length=300, required=True)
    access_token = db.StringField(max_length=300, required=True)
    expires_in = db.IntField(required=True)
    expires_at = db.IntField(required=True)  # EPOCH
    
    def is_valid(self):
        """
        validates agasint EPOCH if token is still valid
        """
        return int(time.time()) < self.expires_at