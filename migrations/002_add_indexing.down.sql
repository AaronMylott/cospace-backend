USE cospace;
ALTER TABLE bookings
DROP FOREIGN KEY bookings_ibfk_2;

DROP INDEX booking_unique
ON bookings;

ALTER TABLE bookings
ADD CONSTRAINT bookings_ibfk_2
FOREIGN KEY (desk_id)
REFERENCES desks(id)
ON DELETE CASCADE;

