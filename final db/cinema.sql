drop database if exists cinema;
create database cinema;
use cinema;
-- Create employees table
CREATE TABLE employees (
  Employee_id INT NOT NULL,
  Employee_name VARCHAR(50) NOT NULL,
  salary DECIMAL(10,2) NOT NULL,
  contact_no VARCHAR(15) DEFAULT NULL,
  date_of_birth DATE DEFAULT NULL,
  PRIMARY KEY (Employee_id)
) ENGINE=InnoDB;



-- Create ticket_vendor table
CREATE TABLE ticket_vendor (
  Employee_id INT NOT NULL,
  PRIMARY KEY (Employee_id),
  CONSTRAINT ticket_vendor_ibfk_1 FOREIGN KEY (Employee_id) REFERENCES employees (Employee_id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- Create customer table
CREATE TABLE customer (
  customer_id INT NOT NULL AUTO_INCREMENT,
  customer_name VARCHAR(255) NOT NULL,
  customer_phone VARCHAR(20) NOT NULL,
  customer_feedback TEXT,
  customer_password VARCHAR(255) NOT NULL DEFAULT 'PASS',
  PRIMARY KEY (customer_id)
) ENGINE=InnoDB;

-- Create hall table
CREATE TABLE hall (
  Hall_ID INT NOT NULL AUTO_INCREMENT,
  Hall_name VARCHAR(100) NOT NULL,
  Capacity INT NOT NULL,
  Availability_status TINYINT(1) DEFAULT '1',
  PRIMARY KEY (Hall_ID)
) ENGINE=InnoDB;

-- Create seat table
CREATE TABLE seat (
  Seat_id INT NOT NULL,
  Seat_Row CHAR(1) NOT NULL,
  Seat_Column INT NOT NULL,
  PRIMARY KEY (Seat_id)
) ENGINE=InnoDB;


-- Create movie table
CREATE TABLE movie (
  MovieID INT NOT NULL,
  MovieName VARCHAR(255) NOT NULL,
  Director VARCHAR(255) DEFAULT NULL,
  Genre VARCHAR(100) DEFAULT NULL,
  Language VARCHAR(50) DEFAULT NULL,
  Release_Date DATE DEFAULT NULL,
  Duration TIME DEFAULT NULL,
  Movie_Description TEXT,
  Price DECIMAL(10,2) DEFAULT NULL,
  PosterPath VARCHAR(255) DEFAULT '/static/img/phphp.jpg',
  Title VARCHAR(255) NOT NULL,
  PRIMARY KEY (MovieID)
) ENGINE=InnoDB;

-- Create movie_show table
CREATE TABLE movie_show (
  ShowID INT NOT NULL AUTO_INCREMENT,
  MovieID INT NOT NULL,
  HallID INT NOT NULL,
  ShowDate DATE NOT NULL,
  ShowTime TIME NOT NULL,
  PRIMARY KEY (ShowID),
  KEY MovieID (MovieID),
  KEY HallID (HallID),
  CONSTRAINT movie_show_ibfk_1 FOREIGN KEY (MovieID) REFERENCES movie (MovieID) ON DELETE CASCADE,
  CONSTRAINT movie_show_ibfk_2 FOREIGN KEY (HallID) REFERENCES hall (Hall_ID) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE hall_seat (
  BookingID INT NOT NULL AUTO_INCREMENT,
  HallID INT NOT NULL,
  SeatID INT NOT NULL,
  ShowID INT NOT NULL,
  IsBooked TINYINT(1) DEFAULT '0',
  PRIMARY KEY (BookingID),
  UNIQUE (SeatID), -- Add unique constraint on SeatID
  KEY HallID (HallID),
  KEY ShowID (ShowID),
  CONSTRAINT hall_seat_ibfk_1 FOREIGN KEY (HallID) REFERENCES hall (Hall_ID) ON DELETE CASCADE,
  CONSTRAINT hall_seat_ibfk_2 FOREIGN KEY (ShowID) REFERENCES movie_show (ShowID) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE Food_item (
    item_id INT AUTO_INCREMENT PRIMARY KEY,
    Item_name VARCHAR(50),
    Quantity_Available INT,
    Price DECIMAL(10, 2)
);


-- Create ticket table
CREATE TABLE ticket (
  TicketID INT NOT NULL AUTO_INCREMENT,
  MovieID INT NOT NULL,
  CustomerID INT NOT NULL,
  HallID INT NOT NULL,
  VendorID INT NOT NULL,
  ShowID INT NOT NULL,
  SeatID INT NOT NULL,
  PRIMARY KEY (TicketID),
  CONSTRAINT ticket_ibfk_1 FOREIGN KEY (SeatID) REFERENCES hall_seat (SeatID) ON DELETE CASCADE,
  CONSTRAINT ticket_ibfk_2 FOREIGN KEY (MovieID) REFERENCES movie (MovieID) ON DELETE CASCADE,
  CONSTRAINT ticket_ibfk_3 FOREIGN KEY (CustomerID) REFERENCES customer (customer_id) ON DELETE CASCADE
) ENGINE=InnoDB;

INSERT INTO Food_item (item_id, Item_name, Quantity_Available, Price )
VALUES 
(1, 'Sodas', 50, 3.00),
(2, 'Fresh Juice', 30, 10.00),
(3, 'Water', 100, 2.00),
(4, 'Caramel Popcorn', 20, 5.00),
(5, 'Butter Popcorn', 25, 5.00),
(6, 'Samosa', 15, 20.00),
(7, 'Spring Roll', 10, 30.00),
(8, 'French Fries', 40, 5.00),
(9, 'Chicken Popcorn', 35, 10.00);

CREATE TABLE Cashier (
    Employee_id INT PRIMARY KEY,
    FOREIGN KEY (Employee_id) REFERENCES Employees(Employee_id),
	cashier_name VARCHAR(50) NOT NULL UNIQUE,
    cashier_password VARCHAR(255) NOT NULL
    
);


INSERT INTO Cashier (Employee_id , cashier_name, cashier_password)
VALUES (1, 'asmaa', '123');




INSERT INTO employees (Employee_id, Employee_name, salary, contact_no, date_of_birth)
VALUES
(1, 'John Doe', 50000.00, '1234567890', '1990-01-01'),
(2, 'Jane Smith', 55000.00, '0987654321', '1988-02-15');

INSERT INTO cashier (Employee_id)
VALUES
(1);

INSERT INTO ticket_vendor (Employee_id)
VALUES
(2);

INSERT INTO customer (customer_name, customer_phone, customer_feedback, customer_password)
VALUES
('Alice', '5551234567', 'Great experience!', 'securepassword1'),
('Bob', '5559876543', 'Average service.', 'securepassword2');

INSERT INTO hall (Hall_ID, Hall_name, Capacity, Availability_status)
VALUES
(1, 'Hall 1', 150, 1),
(2, 'Hall 2', 120, 1),
(3, 'Hall 3', 200, 1),
(4, 'Hall 4', 180, 1),
(5, 'Hall 5', 100, 1),
(6, 'Hall 6', 130, 1),
(7, 'Hall 7', 160, 1),
(8, 'Hall 8', 140, 1),
(9, 'Hall 9', 110, 1),
(10, 'Hall 10', 170, 1);



INSERT INTO seat (Seat_id, Seat_Row, Seat_Column)
VALUES
-- Hall 1
(1, 'A', 1), (2, 'A', 2), (3, 'A', 3), (4, 'A', 4),
(5, 'B', 1), (6, 'B', 2), (7, 'B', 3), (8, 'B', 4),
(9, 'C', 1), (10, 'C', 2), (11, 'C', 3), (12, 'C', 4),
(13, 'D', 1), (14, 'D', 2), (15, 'D', 3), (16, 'D', 4),

-- Hall 2
(17, 'A', 1), (18, 'A', 2), (19, 'A', 3), (20, 'A', 4),
(21, 'B', 1), (22, 'B', 2), (23, 'B', 3), (24, 'B', 4),
(25, 'C', 1), (26, 'C', 2), (27, 'C', 3), (28, 'C', 4),
(29, 'D', 1), (30, 'D', 2), (31, 'D', 3), (32, 'D', 4),

-- Hall 3
(33, 'A', 1), (34, 'A', 2), (35, 'A', 3), (36, 'A', 4),
(37, 'B', 1), (38, 'B', 2), (39, 'B', 3), (40, 'B', 4),
(41, 'C', 1), (42, 'C', 2), (43, 'C', 3), (44, 'C', 4),
(45, 'D', 1), (46, 'D', 2), (47, 'D', 3), (48, 'D', 4),

-- Hall 4
(49, 'A', 1), (50, 'A', 2), (51, 'A', 3), (52, 'A', 4),
(53, 'B', 1), (54, 'B', 2), (55, 'B', 3), (56, 'B', 4),
(57, 'C', 1), (58, 'C', 2), (59, 'C', 3), (60, 'C', 4),
(61, 'D', 1), (62, 'D', 2), (63, 'D', 3), (64, 'D', 4),

-- Hall 5
(65, 'A', 1), (66, 'A', 2), (67, 'A', 3), (68, 'A', 4),
(69, 'B', 1), (70, 'B', 2), (71, 'B', 3), (72, 'B', 4),
(73, 'C', 1), (74, 'C', 2), (75, 'C', 3), (76, 'C', 4),
(77, 'D', 1), (78, 'D', 2), (79, 'D', 3), (80, 'D', 4),

-- Hall 6
(81, 'A', 1), (82, 'A', 2), (83, 'A', 3), (84, 'A', 4),
(85, 'B', 1), (86, 'B', 2), (87, 'B', 3), (88, 'B', 4),
(89, 'C', 1), (90, 'C', 2), (91, 'C', 3), (92, 'C', 4),
(93, 'D', 1), (94, 'D', 2), (95, 'D', 3), (96, 'D', 4),

-- Hall 7
(97, 'A', 1), (98, 'A', 2), (99, 'A', 3), (100, 'A', 4),
(101, 'B', 1), (102, 'B', 2), (103, 'B', 3), (104, 'B', 4),
(105, 'C', 1), (106, 'C', 2), (107, 'C', 3), (108, 'C', 4),
(109, 'D', 1), (110, 'D', 2), (111, 'D', 3), (112, 'D', 4),

-- Hall 8
(113, 'A', 1), (114, 'A', 2), (115, 'A', 3), (116, 'A', 4),
(117, 'B', 1), (118, 'B', 2), (119, 'B', 3), (120, 'B', 4),
(121, 'C', 1), (122, 'C', 2), (123, 'C', 3), (124, 'C', 4),
(125, 'D', 1), (126, 'D', 2), (127, 'D', 3), (128, 'D', 4),

-- Hall 9
(129, 'A', 1), (130, 'A', 2), (131, 'A', 3), (132, 'A', 4),
(133, 'B', 1), (134, 'B', 2), (135, 'B', 3), (136, 'B', 4),
(137, 'C', 1), (138, 'C', 2), (139, 'C', 3), (140, 'C', 4),
(141, 'D', 1), (142, 'D', 2), (143, 'D', 3), (144, 'D', 4),

-- Hall 10
(145, 'A', 1), (146, 'A', 2), (147, 'A', 3), (148, 'A', 4),
(149, 'B', 1), (150, 'B', 2), (151, 'B', 3), (152, 'B', 4),
(153, 'C', 1), (154, 'C', 2), (155, 'C', 3), (156, 'C', 4),
(157, 'D', 1), (158, 'D', 2), (159, 'D', 3), (160, 'D', 4);




INSERT INTO movie_show (ShowID, MovieID, HallID, ShowDate, ShowTime)
VALUES
(1, 1, 1, '2025-01-15', '18:00:00'),
(2, 2, 2, '2025-01-16', '20:00:00'),
(3, 3, 3, '2025-01-17', '19:00:00'),
(4, 4, 4, '2025-01-18', '21:00:00'),
(5, 5, 5, '2025-01-19', '17:30:00'),
(6, 6, 6, '2025-01-20', '20:30:00'),
(7, 7, 7, '2025-01-21', '19:45:00'),
(8, 8, 8, '2025-01-22', '18:15:00'),
(9, 9, 9, '2025-01-23', '20:00:00'),
(10, 10, 10, '2025-01-24', '21:30:00');

INSERT INTO hall_seat (HallID, SeatID, ShowID, IsBooked)
VALUES
-- Hall 1, Show 1
(1, 1, 1, 0), (1, 2, 1, 0), (1, 3, 1, 0), (1, 4, 1, 0),
(1, 5, 1, 0), (1, 6, 1, 0), (1, 7, 1, 0), (1, 8, 1, 0),
(1, 9, 1, 0), (1, 10, 1, 0), (1, 11, 1, 0), (1, 12, 1, 0),
(1, 13, 1, 0), (1, 14, 1, 0), (1, 15, 1, 0), (1, 16, 1, 0),

-- Hall 2, Show 2
(2, 17, 2, 0), (2, 18, 2, 0), (2, 19, 2, 0), (2, 20, 2, 0),
(2, 21, 2, 0), (2, 22, 2, 0), (2, 23, 2, 0), (2, 24, 2, 0),
(2, 25, 2, 0), (2, 26, 2, 0), (2, 27, 2, 0), (2, 28, 2, 0),
(2, 29, 2, 0), (2, 30, 2, 0), (2, 31, 2, 0), (2, 32, 2, 0),

-- Hall 3, Show 3
(3, 33, 3, 0), (3, 34, 3, 0), (3, 35, 3, 0), (3, 36, 3, 0),
(3, 37, 3, 0), (3, 38, 3, 0), (3, 39, 3, 0), (3, 40, 3, 0),
(3, 41, 3, 0), (3, 42, 3, 0), (3, 43, 3, 0), (3, 44, 3, 0),
(3, 45, 3, 0), (3, 46, 3, 0), (3, 47, 3, 0), (3, 48, 3, 0);

INSERT INTO hall_seat (HallID, SeatID, ShowID, IsBooked)
VALUES
-- Hall 4, Show 4
(4, 49, 4, 0), (4, 50, 4, 0), (4, 51, 4, 0), (4, 52, 4, 0),
(4, 53, 4, 0), (4, 54, 4, 0), (4, 55, 4, 0), (4, 56, 4, 0),
(4, 57, 4, 0), (4, 58, 4, 0), (4, 59, 4, 0), (4, 60, 4, 0),
(4, 61, 4, 0), (4, 62, 4, 0), (4, 63, 4, 0), (4, 64, 4, 0),

-- Hall 5, Show 5
(5, 65, 5, 0), (5, 66, 5, 0), (5, 67, 5, 0), (5, 68, 5, 0),
(5, 69, 5, 0), (5, 70, 5, 0), (5, 71, 5, 0), (5, 72, 5, 0),
(5, 73, 5, 0), (5, 74, 5, 0), (5, 75, 5, 0), (5, 76, 5, 0),
(5, 77, 5, 0), (5, 78, 5, 0), (5, 79, 5, 0), (5, 80, 5, 0),

-- Hall 6, Show 6
(6, 81, 6, 0), (6, 82, 6, 0), (6, 83, 6, 0), (6, 84, 6, 0),
(6, 85, 6, 0), (6, 86, 6, 0), (6, 87, 6, 0), (6, 88, 6, 0),
(6, 89, 6, 0), (6, 90, 6, 0), (6, 91, 6, 0), (6, 92, 6, 0),
(6, 93, 6, 0), (6, 94, 6, 0), (6, 95, 6, 0), (6, 96, 6, 0);

INSERT INTO hall_seat (HallID, SeatID, ShowID, IsBooked)
VALUES
-- Hall 7, Show 7
(7, 97, 7, 0), (7, 98, 7, 0), (7, 99, 7, 0), (7, 100, 7, 0),
(7, 101, 7, 0), (7, 102, 7, 0), (7, 103, 7, 0), (7, 104, 7, 0),
(7, 105, 7, 0), (7, 106, 7, 0), (7, 107, 7, 0), (7, 108, 7, 0),
(7, 109, 7, 0), (7, 110, 7, 0), (7, 111, 7, 0), (7, 112, 7, 0),

-- Hall 8, Show 8
(8, 113, 8, 0), (8, 114, 8, 0), (8, 115, 8, 0), (8, 116, 8, 0),
(8, 117, 8, 0), (8, 118, 8, 0), (8, 119, 8, 0), (8, 120, 8, 0),
(8, 121, 8, 0), (8, 122, 8, 0), (8, 123, 8, 0), (8, 124, 8, 0),
(8, 125, 8, 0), (8, 126, 8, 0), (8, 127, 8, 0), (8, 128, 8, 0),

-- Hall 9, Show 9
(9, 129, 9, 0), (9, 130, 9, 0), (9, 131, 9, 0), (9, 132, 9, 0),
(9, 133, 9, 0), (9, 134, 9, 0), (9, 135, 9, 0), (9, 136, 9, 0),
(9, 137, 9, 0), (9, 138, 9, 0), (9, 139, 9, 0), (9, 140, 9, 0),
(9, 141, 9, 0), (9, 142, 9, 0), (9, 143, 9, 0), (9, 144, 9, 0),

-- Hall 10, Show 10
(10, 145, 10, 0), (10, 146, 10, 0), (10, 147, 10, 0), (10, 148, 10, 0),
(10, 149, 10, 0), (10, 150, 10, 0), (10, 151, 10, 0), (10, 152, 10, 0),
(10, 153, 10, 0), (10, 154, 10, 0), (10, 155, 10, 0), (10, 156, 10, 0),
(10, 157, 10, 0), (10, 158, 10, 0), (10, 159, 10, 0), (10, 160, 10, 0);


INSERT INTO movie (MovieID, MovieName, Director, Language, Title, Genre, Release_Date, Duration, Movie_Description, PosterPath)
VALUES
(1, 'Avatar', 'James Cameron', 'English', 'Avatar', 'Sci-Fi', '2009-12-18', '02:42:00', 'A Marine on Pandora.', '/static/img/photo1.jpg'),
(2, 'The Godfather', 'Francis Ford Coppola', 'English', 'The Godfather', 'Crime', '1972-03-24', '02:55:00', 'Mafia family story.', '/static/img/photo2.jpg'),
(3, 'The Dark Knight', 'Christopher Nolan', 'English', 'The Dark Knight', 'Action', '2008-07-18', '02:32:00', 'Batman fights Joker.', '/static/img/photo3.jpg'),
(4, 'Inception', 'Christopher Nolan', 'English', 'Inception', 'Sci-Fi', '2010-07-16', '02:28:00', 'Dreams within dreams.', '/static/img/photo4.jpg'),
(5, 'Titanic', 'James Cameron', 'English', 'Titanic', 'Romance', '1997-12-19', '03:15:00', 'Love story on the Titanic.', '/static/img/photo5.jpg'),
(6, 'Interstellar', 'Christopher Nolan', 'English', 'Interstellar', 'Sci-Fi', '2014-11-07', '02:49:00', 'Exploration of space.', '/static/img/photo6.jpg'),
(7, 'Pulp Fiction', 'Quentin Tarantino', 'English', 'Pulp Fiction', 'Crime', '1994-10-14', '02:34:00', 'Intertwining stories.', '/static/img/photo7.webp'),
(8, 'The Matrix', 'Lana Wachowski', 'English', 'The Matrix', 'Sci-Fi', '1999-03-31', '02:16:00', 'Virtual reality world.', '/static/img/photo8.jpg'),
(9, 'Forrest Gump', 'Robert Zemeckis', 'English', 'Forrest Gump', 'Drama', '1994-07-06', '02:22:00', 'Life story of Forrest.', '/static/img/photo9.jpg'),
(10, 'The Avengers', 'Joss Whedon', 'English', 'The Avengers', 'Action', '2012-05-04', '02:23:00', 'Superheroes team up.', '/static/img/photo10.jpg');





