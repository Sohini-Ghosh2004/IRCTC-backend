from app.models.train_schedule import TrainSchedule
from app.models.booking import Booking
from app.extensions import db
from app.schemas.booking_schema import BookingSchema

def book_ticket_service(user_id,schedule_id):
    # schedule=TrainSchedule.query.get(data["train_schedule_id"])
    schedule=(db.session.query(TrainSchedule)
            .filter_by(train_schedule_id=schedule_id)
            .with_for_update()       #row locking
            .first()
            )
    if not schedule:
        return None,"Schedule not found"
    
    #duplicate booking check
    existing=Booking.query.filter(
        Booking.user_id == user_id,
        Booking.train_schedule_id == schedule_id,
        Booking.status.in_(["CONFIRMED", "WAITLIST","RAC"])
    ).first()
    if existing:
        return None, "Already booked"
    
    # confirmed or waitlist 
    if schedule.available_seats > 0:
        confirmed_count = Booking.query.filter(
            Booking.train_schedule_id == schedule_id,
            Booking.status == "CONFIRMED"
        ).count()
        booking=Booking(
            user_id=user_id,
            train_schedule_id=schedule_id,
            seat_number=confirmed_count +1,
            status="CONFIRMED"
        )
        schedule.available_seats-=1
    else:
        rac_count = Booking.query.filter(
            Booking.train_schedule_id == schedule_id,
            Booking.status == "RAC"
        ).count()

        if rac_count < schedule.rac_capacity:
            booking = Booking(
                user_id=user_id,
                train_schedule_id=schedule_id,
                status="RAC",
                rac_number=rac_count + 1
            )   
        
        else: #assign waitlist number
            wl_count = Booking.query.filter(
                Booking.train_schedule_id == schedule_id,
                Booking.status == "WAITLIST"
            ).count()
            booking=Booking(
                user_id=user_id,
                train_schedule_id=schedule_id,
                status="WAITLIST",
                waitlist_number=wl_count+1
            )
        
    db.session.add(booking)
    db.session.commit()
    return booking, None


def cancel_booking_service(user_id, booking_id):

    booking = Booking.query.filter_by(
        booking_id=booking_id,
        user_id=user_id
    ).first()

    if not booking:
        return None, "Booking not found"
    
    if booking.status == "CANCELLED":
        return None, "Already cancelled"
    
    # lock schedule
    schedule = (db.session.query(TrainSchedule)
        .filter_by(train_schedule_id=booking.train_schedule_id)
        .with_for_update()
        .first()
    )
    original_status = booking.status
    booking.status = "CANCELLED"
    db.session.flush()

    # CASE 1: CONFIRMED CANCEL
    if original_status == "CONFIRMED":

        rac_user = Booking.query.filter(
            Booking.train_schedule_id == schedule.train_schedule_id,
            Booking.status == "RAC"
        ).order_by(Booking.rac_number).first()

        if rac_user:
            # promote RAC → CONFIRMED
            rac_user.status = "CONFIRMED"
            rac_user.seat_number = booking.seat_number
            rac_user.rac_number = None

            #shift remaining RAC
            racs = Booking.query.filter(
                Booking.train_schedule_id == schedule.train_schedule_id,
                Booking.status == "RAC"
            ).order_by(Booking.rac_number).all()

            for i, r in enumerate(racs, start=1):
                r.rac_number = i

            # WAITLIST → RAC 
            wl_user = Booking.query.filter(
                Booking.train_schedule_id == schedule.train_schedule_id,
                Booking.status == "WAITLIST"
            ).order_by(Booking.waitlist_number).first()

            if wl_user:
                wl_user.status = "RAC"
                wl_user.rac_number = len(racs) + 1
                wl_user.waitlist_number = None

        else:
            # no RAC 
            schedule.available_seats += 1

    
    # CASE 2: RAC CANCEL
    
    elif original_status == "RAC":

        # shift remaining RAC
        racs = Booking.query.filter(
            Booking.train_schedule_id == schedule.train_schedule_id,
            Booking.status == "RAC"
        ).order_by(Booking.rac_number).all()

        for i, r in enumerate(racs, start=1):
            r.rac_number = i

        # WAITLIST → RAC
        wl_user = Booking.query.filter(
            Booking.train_schedule_id == schedule.train_schedule_id,
            Booking.status == "WAITLIST"
        ).order_by(Booking.waitlist_number).first()

        if wl_user:
            wl_user.status = "RAC"
            wl_user.rac_number = len(racs) + 1
            wl_user.waitlist_number = None

   
    # CASE 3: WAITLIST CANCEL, REORDER WAITLIST 
    wls = Booking.query.filter(
        Booking.train_schedule_id == schedule.train_schedule_id,
        Booking.status == "WAITLIST"
    ).order_by(Booking.waitlist_number).all()

    for i, w in enumerate(wls, start=1):
        w.waitlist_number = i

    db.session.commit()

    return booking, None



def get_bookings_service(user_id):
    bookings=Booking.query.filter_by(user_id=user_id)\
        .order_by(Booking.booking_id.desc()).all()
    schema=BookingSchema(many=True)
    result=schema.dump(bookings)
    return result,None