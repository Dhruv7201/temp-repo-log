from marshmallow import Schema, fields


class VendResponseSchema(Schema):
    MachineNo = fields.String()
    SR_No = fields.String()
    VendingStatus = fields.String()
    OPDD_ID = fields.String()


class VendResponseArraySchema(Schema):
    itemlist = fields.List(fields.Nested(VendResponseSchema))
