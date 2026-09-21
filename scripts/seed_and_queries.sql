USE cospace;

INSERT INTO teams(name, department)
VALUES
('Development', 'Technology'),
('HR', 'People'),                   --#Inserts all the teams information
('Sales', 'Commercial');

INSERT INTO users(first_name, last_name, email, team_id)
VALUES
('Bill', 'Gates', 'bill@example.com', 1),
('Ada', 'Lovelace', 'ada@example.com', 1),
('Grace', 'Hopper', 'grace@example.com', 1),
('Alan', 'Turing', 'alan@example.com', 1),
('Sarah', 'Jones', 'sarah@example.com', 2),             --#Inserts all the user information
('Tom', 'Brown', 'tom@example.com', 2),
('Emma', 'Wilson', 'emma@example.com', 3),
('James', 'Smith', 'james@example.com', 3);

INSERT INTO rooms(name, capacity)
VALUES
('Room1', 4),
('Room2', 8),                  --#Inserts all the rooms information
('Room3', 12);

INSERT INTO desks(name, floor)
VALUES
('Desk A', 1),
('Desk B', 1),                  --# Inserts all the desk data
('Desk C', 2),
('Desk D', 2);

INSERT INTO bookings(user_id, desk_id, rooms_id, booking_date)
VALUES
(1, 1, 1, '2026-09-01'),
(1, 1, 1, '2026-09-02'),
(2, 2, 2, '2026-09-01'),                            --#Inserts all the bookings data
(3, 3, 3, '2026-09-01'),
(5, 4, 1, '2026-09-01'),
(7, 2, 2, '2026-09-03');

SELECT CONCAT_WS(' ',u.first_name,u.last_name)as full_name,
    t.name as team_name,
    Count(b.id) as total_bookings
   From users u
   LEFT JOIN teams t     --#Shows full name concatenated with their team name and how many desk bookings they have
   ON u.team_id = t.id
   LEFT JOIN bookings b
   ON u.id = b.user_id
GROUP BY u.id, u.first_name, u.last_name, t.name;   

UPDATE users
SET team_id = 2
WHERE first_name = "Bill"; --#Updtes Bills team id to 2 to put him in the HR team

DELETE FROM desks 
where id = 3; --#Deletes the desk with the id 3 and deletes all booking related to it due to the foreign key
