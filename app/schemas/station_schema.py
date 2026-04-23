from marshmallow import Schema,fields

class TrainResultSchema(Schema):
    train = fields.Dict()
    schedule_id = fields.Int()
    route = fields.Dict()
    timing = fields.Dict()
    available_seats = fields.Int()