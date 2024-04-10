from marshmallow import Schema, fields

class ObjectSchema(Schema):
    id = fields.Str()
    title = fields.Str()
    content = fields.Str()
    published_on = fields.Str()
    link = fields.Str()
    source = fields.Str()