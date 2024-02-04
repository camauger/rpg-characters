from mongoengine import Document, StringField

class Clothing(Document):
    name = StringField(required=True)
    description = StringField()
    meta = {'collection': 'clothing'}
