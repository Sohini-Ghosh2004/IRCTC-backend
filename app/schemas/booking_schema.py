from marshmallow import Schema, fields,ValidationError,post_dump

class BookingSchema(Schema):
    booking_id = fields.Int() 
    train_schedule_id = fields.Int()
    status = fields.Str()
    seat_number = fields.Int(allow_none=True)
    waitlist_number = fields.Int(allow_none=True)
    rac_number = fields.Int(allow_none=True)

    @post_dump
    def remove_irrelevant_fields(self, data, **kwargs):
        if data["status"] == "CONFIRMED":
            data.pop("waitlist_number", None)
            data.pop("rac_number", None)

        elif data["status"] == "WAITLIST":
            data.pop("seat_number", None)
            data.pop("rac_number", None)

        elif data["status"] == "RAC":
            data.pop("seat_number", None)
            data.pop("waitlist_number", None)
               
        return data

class BookingCreateSchema(Schema):
    train_schedule_id=fields.Int(required=True)
  