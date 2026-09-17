USE cospace;
CREATE UNIQUE INDEX booking_unique
ON bookings (desk_id, booking_date);

