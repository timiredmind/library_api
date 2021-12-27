from marshmallow import fields, Schema


class AuthorSchema(Schema):
    class Meta:
        ordered = True

    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    description = fields.Str()
