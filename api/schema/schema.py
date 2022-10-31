from api import ma, restApp
from marshmallow import fields


class UserSchema(ma.Schema):
    class Meta:
        fields = ["_id",
                  "id",
                  "name",
                  "age",
                  "emails",
                  "createdInMS",
                  "updatedInMS",
                  "createdBy",
                  "updatedBy"]

    _id = fields.Str(required=True)
    id = fields.Int(required=True)
    name = fields.Str(required=True)
    age = fields.Int(required=True, default=18)
    emails = fields.List(fields.Str,required=True,default=[])

    # Audit
    createdInMS = fields.Int(required=True)
    createdBy = fields.Str(required=True)
    updatedInMS = fields.Int(required=True)
    updatedBy = fields.Str(required=True)
