import pymysql
from flask import Flask, request, render_template, redirect, url_for, jsonify, flash, session
from flask_sqlalchemy import SQLAlchemy
import mysql.connector

# Set the secret key to some random bytes. Keep this really secret!
app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:asmaa@localhost/cinema'
db = SQLAlchemy(app)


def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='asmaa',
        database='cinema',
        port=3306
    )

def fetch_movies():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = """
    SELECT MovieID, MovieName, Director, Language, Genre, Release_Date, Duration, Movie_Description, PosterPath
    FROM Movie
    """
    cursor.execute(query)
    movies = cursor.fetchall()
    for movie in movies:
        if not movie.get('PosterPath'):
            movie['PosterPath'] = '/static/img/default-poster.jpg'
    connection.close()
    return movies

@app.route('/')
def home():
    return render_template('index.html')
# Placeholder route for the next operation after login

@app.route('/next_operation')
def next_operation():
    movies = fetch_movies()
    return render_template('movieShow.html', movies=movies)

# Route for the before login page
@app.route('/beforeLog')
def beforeLog():
    return render_template('beforeLog.html')
  

# Route for the ticket vendor login page
@app.route('/Tlog')
def Tlog():
    return render_template('Tlog.html')

# Route to handle ticket vendor login
@app.route('/ticketvendorlogin', methods=['POST'])
def ticketvendorlogin():
    username = request.form['name']
    password = request.form['pass']
    
    if username == 'john' and password == '012345678':
        flash('Login successful!', 'success')
        return redirect(url_for('Tmanager'))
    else:
        flash('Invalid username or password', 'danger')
        return redirect(url_for('Tlog'))

# Route for the ticket manager page
@app.route('/Tmanager')
def Tmanager():
    return render_template('Tmanager.html')

# Route for the home page
@app.route('/home')
def Chome():
    return render_template('home.html')

###############################

# Route to add a new customer
@app.route('/add_customer', methods=['GET', 'POST'])
def add_customer():
    if request.method == 'POST':
        customer_name = request.form['customer_name']
        customer_phone = request.form['customer_phone']
        customer_feedback = request.form['customer_feedback']
        customer_password = request.form['customer_password']

        try:
            connection = pymysql.connect(
                host='localhost',
                user='root',
                password='asmaa',
                database='cinema',
                port=3306
            )
            cursor = connection.cursor()
            cursor.execute(
                """
                INSERT INTO Customer (customer_name, customer_phone, customer_feedback, customer_password)
                VALUES (%s, %s, %s, %s)
                """,
                (customer_name, customer_phone, customer_feedback, customer_password),
            )
            connection.commit()
            cursor.close()
            connection.close()
            flash('Customer added successfully!', 'success')
            return redirect('/list_customers')
        except pymysql.MySQLError as e:
            flash(f"Error: {e}", 'danger')

    return render_template('add_customer.html')

# Route to list all customers
@app.route('/list_customers')
def list_customers():
    try:
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='asmaa',
            database='cinema',
            port=3306
        )
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM Customer")
        customers = cursor.fetchall()
        cursor.close()
        connection.close()
        return render_template('list_customers.html', customers=customers)
    except pymysql.MySQLError as e:
        return f"Error: {e}"

# Route to delete a customer
@app.route('/delete_customer/<int:customer_id>', methods=['POST'])
def delete_customer(customer_id):
    try:
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='asmaa',
            database='cinema',
            port=3306
        )
        cursor = connection.cursor()
        cursor.execute("DELETE FROM Customer WHERE customer_id = %s", (customer_id,))
        connection.commit()
        cursor.close()
        connection.close()
        return redirect('/list_customers')
    except pymysql.MySQLError as e:
        return f"Error: {e}"

# Route to update a customer's information
@app.route('/update_customer/<int:customer_id>', methods=['GET', 'POST'])
def update_customer(customer_id):
    if request.method == 'POST':
        customer_name = request.form['customer_name']
        customer_phone = request.form['customer_phone']
        customer_feedback = request.form['customer_feedback']

        try:
            connection = pymysql.connect(
                host='localhost',
                user='root',
                password='asmaa',
                database='cinema',
                port=3306
            )
            cursor = connection.cursor()
            cursor.execute(
                """
                UPDATE Customer 
                SET customer_name = %s, customer_phone = %s, customer_feedback = %s 
                WHERE customer_id = %s
                """,
                (customer_name, customer_phone, customer_feedback, customer_id),
            )
            connection.commit()
            cursor.close()
            connection.close()
            return redirect('/list_customers')
        except pymysql.MySQLError as e:
            return f"Error: {e}"

    try:
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='asmaa',
            database='cinema',
            port=3306
        )
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM Customer WHERE customer_id = %s", (customer_id,))
        customer = cursor.fetchone()
        cursor.close()
        connection.close()

        if customer:
            return render_template('update_customer.html', customer=customer)
        else:
            return "Customer not found."
    except pymysql.MySQLError as e:
        return f"Error: {e}"

# Route to search customers by name
@app.route('/search_customer', methods=['GET', 'POST'])
def search_customer():
    if request.method == 'POST':
        search_query = request.form['search_query']
        try:
            connection = pymysql.connect(
                host='localhost',
                user='root',
                password='asmaa',
                database='cinema',
                port=3306
            )
            cursor = connection.cursor(pymysql.cursors.DictCursor)
            cursor.execute(
                "SELECT * FROM Customer WHERE customer_name LIKE %s", 
                (f"%{search_query}%",)
            )
            customers = cursor.fetchall()
            cursor.close()
            connection.close()
            return render_template('list_customers.html', customers=customers)
        except pymysql.MySQLError as e:
            return f"Error: {e}"

    return render_template('search_customer.html')


# Route for customer login
@app.route('/Clog', methods=['GET', 'POST'])
def customerlogin():
    if request.method == 'POST':
        username = request.form['name']
        password = request.form['pass']
        try:
            connection = pymysql.connect(
                host='localhost',
                user='root',
                password='asmaa',
                database='cinema',
                port=3306
            )
            cursor = connection.cursor()
            cursor.execute("SELECT customer_password FROM Customer WHERE customer_name = %s", (username,))
            result = cursor.fetchone()
            cursor.close()
            connection.close()
            if result and result[0] == password:
                flash('Login successful!', 'success')
                return redirect(url_for('next_operation'))
            else:
                flash('Invalid username or password', 'danger')
        except pymysql.MySQLError as e:
            flash(f"Error: {e}", 'danger')
    return render_template('Clog.html')

# Route for customer registration
@app.route('/customerregister', methods=['GET', 'POST'])
def customerregister():
    if request.method == 'POST':
        customer_name = request.form['reg_name']
        customer_phone = request.form['reg_phone']
        customer_password = request.form['reg_pass']
        confirm_password = request.form['confirm_pass']
        if customer_password == confirm_password:
            try:
                connection = pymysql.connect(
                    host='localhost',
                    user='root',
                    password='asmaa',
                    database='cinema',
                    port=3306
                )
                cursor = connection.cursor()
                cursor.execute(
                    """
                    INSERT INTO Customer (customer_name, customer_phone, customer_feedback, customer_password)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (customer_name, customer_phone, 'No feedback yet', customer_password)
                )
                connection.commit()
                cursor.close()
                connection.close()
                flash('Registration successful! Please log in.', 'success')
                return redirect(url_for('customerlogin'))
            except pymysql.MySQLError as e:
                flash(f"Error: {e}", 'danger')
        else:
            flash('Passwords do not match', 'danger')
    return render_template('Cregister.html')




def fetch_movie_schedule(movie_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        query = """
        SELECT 
            ms.ShowID,
            h.Hall_ID, 
            h.Hall_name, 
            h.Capacity, 
            ms.ShowDate AS Date, 
            ms.ShowTime AS Time,
            CASE 
                WHEN (
                    SELECT COUNT(*) 
                    FROM hall_seat 
                    WHERE hall_seat.ShowID = ms.ShowID AND hall_seat.IsBooked = TRUE
                ) = h.Capacity THEN 0
                ELSE 1
            END AS Availability_status
        FROM movie_show ms
        JOIN Hall h ON h.Hall_ID = ms.HallID
        WHERE ms.MovieID = %s
        """
        cursor.execute(query, (movie_id,))
        schedule = cursor.fetchall()
    finally:
        cursor.close()
        connection.close()
    return schedule

@app.route('/booking/<int:movie_id>')
def booking_page(movie_id):
    schedule = fetch_movie_schedule(movie_id)
    movie_name = next((movie['MovieName'] for movie in fetch_movies() if movie['MovieID'] == movie_id), "Unknown Movie")
    return render_template('movie_schedule.html', schedule=schedule, movie_name=movie_name)

@app.route('/final-book/<int:movie_id>/<hall_name>', methods=['GET', 'POST'])
def final_book(movie_id, hall_name):
 
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        hall_query = "SELECT Hall_ID FROM Hall WHERE Hall_name = %s"
        cursor.execute(hall_query, (hall_name,))
        hall_id = cursor.fetchone()

        if not hall_id:
            return "Invalid Hall Name!"

        check_query = """
        SELECT COUNT(*) FROM Ticket
        WHERE CustomerID = %s AND MovieID = %s AND HallID = %s
        """
        cursor.execute(check_query, ( movie_id, hall_id['Hall_ID']))
        exists = cursor.fetchone()['COUNT(*)']

        if exists > 0:
            return "You have already booked this movie in this hall!"

        insert_query = """
        INSERT INTO Ticket (MovieID, CustomerID, HallID, Date, Time, Price)
        VALUES (%s, %s, %s, CURDATE(), CURTIME(), 10.00)
        """
        cursor.execute(insert_query, (movie_id , hall_id['Hall_ID']))
        connection.commit()

    finally:
        cursor.close()
        connection.close()

    return redirect(url_for('movie_list'))

@app.route('/movie-schedule/<int:movie_id>')
def movie_schedule(movie_id):
    customer_id = request.args.get('customer_id', None)

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        query = """
        SELECT 
            ms.ShowID,
            h.Hall_ID, 
            h.Hall_name, 
            h.Capacity, 
            ms.ShowDate AS Date, 
            ms.ShowTime AS Time,
            CASE 
                WHEN (
                    SELECT COUNT(*) 
                    FROM hall_seat 
                    WHERE hall_seat.ShowID = ms.ShowID AND hall_seat.IsBooked = TRUE
                ) = h.Capacity THEN 0
                ELSE 1
            END AS Availability_status
        FROM movie_show ms
        JOIN Hall h ON h.Hall_ID = ms.HallID
        WHERE ms.MovieID = %s
        """
        cursor.execute(query, (movie_id,))
        schedule = cursor.fetchall() or []  # Default to empty list if no results

        movie_query = "SELECT MovieName FROM Movie WHERE MovieID = %s"
        cursor.execute(movie_query, (movie_id,))
        movie_result = cursor.fetchone()
        movie_name = movie_result['MovieName'] if movie_result else 'Unknown Movie'

    finally:
        cursor.close()
        connection.close()

    return render_template(
        'movie_schedule.html',
        movie_id=movie_id,
        movie_name=movie_name,
        schedule=schedule,
        customer_id=customer_id
    )



@app.route('/movie/<int:movie_id>')
def movie_details(movie_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        query = """
        SELECT MovieID, MovieName, Director, Genre, Language, Release_Date, Duration, Movie_Description, PosterPath, price
        FROM Movie
        WHERE MovieID = %s
        """
        cursor.execute(query, (movie_id,))
        movie = cursor.fetchone()

        if movie:
            print("Fetched Movie:", movie)  # طباعة للتصحيح
            return render_template('movie_details.html', movie=movie)
        else:
            print("Movie not found")
            return "Movie not found", 404
    except Exception as e:
        print("Error occurred:", e)
        return f"An error occurred: {e}", 500
    finally:
        connection.close()

@app.route('/api/movies/<int:movie_id>', methods=['GET'])
def get_movie(movie_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        query = "SELECT * FROM Movie WHERE MovieID = %s"
        cursor.execute(query, (movie_id,))
        movie = cursor.fetchone()
        if movie:
            return jsonify(movie)
        else:
            return jsonify({"error": "Movie not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/managmentMovie')
def management_movie():
    return render_template('managmentMovie.html')

@app.route('/api/movies', methods=['GET'])
def get_movies():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        query = """
        SELECT MovieID, MovieName, Director, Language, Title, Genre, Release_Date, Duration, Movie_Description, Price, PosterPath
        FROM Movie
        """
        cursor.execute(query)
        movies = cursor.fetchall()
        return jsonify(movies)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        connection.close()


@app.route('/api/movies', methods=['POST'])
def add_movie():
    data = request.json 
    connection = get_db_connection()
    cursor = connection.cursor()
    
    query = """
        INSERT INTO Movie (MovieID, MovieName, Director, Language, Title, Genre, Release_Date, Duration, Movie_Description, PosterPath, Price)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
           """
    
    try:
        cursor.execute(query, (
            data['MovieID'],          
            data['MovieName'],        
            data['Director'],          
            data['Language'],         
            data['Title'],             
            data['Genre'],            
            data['Release_Date'],      
            data['Duration'],          
            data['Movie_Description'],
            data['PosterPath'],
             data['price']
        ))
        connection.commit()
        return jsonify({"message": "Movie added successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/api/movies/<int:movie_id>', methods=['PUT'])
def update_movie(movie_id):
    try:
        data = request.json
        connection = get_db_connection()
        cursor = connection.cursor()
        query = """
            UPDATE Movie
            SET MovieName = %s, Director = %s, Genre = %s, Language = %s, 
                Release_Date = %s, Duration = %s, Price = %s, PosterPath = %s
            WHERE MovieID = %s
        """
        cursor.execute(query, (
            data['MovieName'], data['Director'], data['Genre'],
            data['Language'], data['Release_Date'], data['Duration'],
            data['Price'], data['PosterPath'], movie_id
        ))
        connection.commit()
        return jsonify({"message": "Movie updated successfully!"}), 200
    except Exception as e:
        print("Error:", e)  
        return jsonify({"error": str(e)}), 500
    finally:
        connection.close()


@app.route('/api/movies/<int:movie_id>', methods=['DELETE'])
def delete_movie(movie_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    query = "DELETE FROM Movie WHERE MovieID = %s"
    cursor.execute(query, (movie_id,))
    connection.commit()
    connection.close()
    return jsonify({"message": "Movie deleted successfully!"})

@app.route('/api/movies/search', methods=['GET'])
def search_movies():
    attribute = request.args.get('attribute')
    value = request.args.get('value')

    allowed_attributes = ['MovieID', 'MovieName', 'Director', 'Language', 'Title', 'Genre', 'Release_Date', 'Duration', 'Movie_Description', 'PosterPath', 'Price']

    if attribute not in allowed_attributes:
        return jsonify({"error": f"Invalid attribute: {attribute}"}), 400

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        query = f"SELECT * FROM Movie WHERE {attribute} LIKE %s"
        cursor.execute(query, ('%' + value + '%',))
        movies = cursor.fetchall()
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        connection.close()

    return jsonify(movies)


@app.route('/manage-movies')
def manage_movies():
    return render_template('managmentMovie.html')
@app.route('/update-movie', methods=['GET'])
def update_movie_page():
    movie_id = request.args.get('movie_id')  
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    query = "SELECT * FROM Movie WHERE MovieID = %s"
    cursor.execute(query, (movie_id,))
    movie = cursor.fetchone()
    connection.close()

    if movie:
        return render_template('Update.html', movie=movie)
    else:
        return "Movie not found", 404
@app.route('/hall-seats/<int:show_id>')
def hall_seats(show_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
    SELECT 
        hs.SeatID, 
        hs.IsBooked, 
        s.Seat_Row, 
        s.Seat_Column
    FROM hall_seat hs
    JOIN seat s ON hs.SeatID = s.Seat_id
    WHERE hs.ShowID = %s
    """
    cursor.execute(query, (show_id,))
    seats = cursor.fetchall()

    connection.close()

    return render_template('hall_seats.html', seats=seats, show_id=show_id)


@app.route('/book-seats', methods=['POST'])
def book_seats():
    data = request.json
    seat_id = data.get('seat_id')
    show_id = data.get('show_id')

    if not seat_id or not show_id:
        return jsonify({"error": "Missing required data"}), 400

    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        query = """
        UPDATE hall_seat 
        SET IsBooked = TRUE 
        WHERE SeatID = %s AND ShowID = %s
        """
        cursor.execute(query, (seat_id, show_id))
        connection.commit()
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        connection.close()

def fetch_total_customers():
    connection = get_db_connection()
    cursor = connection.cursor()
    query = "SELECT COUNT(*) AS Total_Customers FROM customer"
    cursor.execute(query)
    total_customers = cursor.fetchone()[0]  # Retrieve the count from the result
    connection.close()
    return total_customers


def fetch_total_bookings():
    connection = get_db_connection()
    cursor = connection.cursor()
    query = """
    SELECT COUNT(*) AS Total_Bookings
    FROM hall_seat
    WHERE IsBooked = 1
    """
    cursor.execute(query)
    total_bookings = cursor.fetchone()[0]
    connection.close()
    return total_bookings


def fetch_movies_available():
    connection = get_db_connection()
    cursor = connection.cursor()
    query = "SELECT COUNT(*) AS Movies_Available FROM movie"
    cursor.execute(query)
    movies_available = cursor.fetchone()[0]
    connection.close()
    return movies_available


def fetch_recent_customers(limit=5):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = """
    SELECT customer_id AS CustomerID, customer_name AS FirstName, 
           customer_phone AS Phone, customer_feedback AS Feedback
    FROM customer
    ORDER BY customer_id DESC
    LIMIT %s
    """
    cursor.execute(query, (limit,))
    recent_customers = cursor.fetchall()
    connection.close()
    return recent_customers


def fetch_bookings_per_month():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = """
    SELECT DATE_FORMAT(ms.ShowDate, '%Y-%m') AS Month, COUNT(hs.BookingID) AS Total_Bookings
    FROM movie_show ms
    JOIN hall_seat hs ON ms.ShowID = hs.ShowID
    WHERE hs.IsBooked = 1
    GROUP BY DATE_FORMAT(ms.ShowDate, '%Y-%m')
    ORDER BY Month DESC
    """
    cursor.execute(query)
    bookings_per_month = cursor.fetchall()
    connection.close()
    return bookings_per_month


def fetch_total_revenue():
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        # Fetch ticket revenue
        ticket_query = """
        SELECT SUM(m.Price) AS TotalTicketRevenue
        FROM movie_show ms
        JOIN hall_seat hs ON ms.ShowID = hs.ShowID
        JOIN movie m ON ms.MovieID = m.MovieID
        WHERE hs.IsBooked = 1
        """
        cursor.execute(ticket_query)
        total_ticket_revenue = cursor.fetchone()[0] or 0

        # Fetch food revenue (if you track food revenue separately)
        food_query = "SELECT SUM(Price * Quantity_Available) AS TotalFoodRevenue FROM Food_item"
        cursor.execute(food_query)
        total_food_revenue = cursor.fetchone()[0] or 0
    finally:
        connection.close()

    return {
        "ticket_revenue": total_ticket_revenue,
        "food_revenue": total_food_revenue,
        "total_revenue": total_ticket_revenue + total_food_revenue
    }


def fetch_peak_booking_times(limit=5):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = """
    SELECT TIME(ms.ShowTime) AS BookingTime, COUNT(hs.BookingID) AS TotalBookings
    FROM movie_show ms
    JOIN hall_seat hs ON ms.ShowID = hs.ShowID
    WHERE hs.IsBooked = 1
    GROUP BY TIME(ms.ShowTime)
    ORDER BY TotalBookings DESC
    LIMIT %s
    """
    cursor.execute(query, (limit,))
    peak_times = cursor.fetchall()
    connection.close()
    return peak_times


def fetch_most_active_customers(limit=5):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = """
    SELECT c.customer_id AS CustomerID, c.customer_name AS CustomerName, COUNT(hs.BookingID) AS TotalBookings
    FROM customer c
    JOIN ticket t ON c.customer_id = t.CustomerID
    JOIN hall_seat hs ON t.SeatID = hs.SeatID
    WHERE hs.IsBooked = 1
    GROUP BY c.customer_id, c.customer_name
    ORDER BY TotalBookings DESC
    LIMIT %s
    """
    cursor.execute(query, (limit,))
    active_customers = cursor.fetchall()
    connection.close()
    return active_customers

def fetch_peak_revenue_days(limit=5):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = """
    SELECT ms.ShowDate AS RevenueDay, SUM(m.Price) AS TotalRevenue
    FROM movie_show ms
    JOIN hall_seat hs ON ms.ShowID = hs.ShowID
    JOIN movie m ON ms.MovieID = m.MovieID
    WHERE hs.IsBooked = 1
    GROUP BY ms.ShowDate
    ORDER BY TotalRevenue DESC
    LIMIT %s
    """
    cursor.execute(query, (limit,))
    peak_revenue_days = cursor.fetchall()
    connection.close()
    return peak_revenue_days

def fetch_most_popular_movies(limit=5):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = """
    SELECT m.MovieName, COUNT(hs.BookingID) AS TotalTicketsSold
    FROM movie m
    JOIN movie_show ms ON m.MovieID = ms.MovieID
    JOIN hall_seat hs ON ms.ShowID = hs.ShowID
    WHERE hs.IsBooked = 1
    GROUP BY m.MovieID, m.MovieName
    ORDER BY TotalTicketsSold DESC
    LIMIT %s
    """
    cursor.execute(query, (limit,))
    popular_movies = cursor.fetchall()
    connection.close()
    return popular_movies

def fetch_hall_utilization_rate():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = """
    SELECT h.Hall_name, 
           COUNT(CASE WHEN hs.IsBooked = 1 THEN 1 END) / COUNT(*) * 100 AS UtilizationRate
    FROM hall h
    JOIN hall_seat hs ON h.Hall_ID = hs.HallID
    GROUP BY h.Hall_ID, h.Hall_name
    ORDER BY UtilizationRate DESC
    """
    cursor.execute(query)
    utilization_data = cursor.fetchall()
    connection.close()
    return utilization_data

def fetch_revenue_per_genre():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = """
    SELECT m.Genre, SUM(m.Price) AS TotalRevenue
    FROM movie m
    JOIN movie_show ms ON m.MovieID = ms.MovieID
    JOIN hall_seat hs ON ms.ShowID = hs.ShowID
    WHERE hs.IsBooked = 1
    GROUP BY m.Genre
    ORDER BY TotalRevenue DESC
    """
    cursor.execute(query)
    revenue_per_genre = cursor.fetchall()
    connection.close()
    return revenue_per_genre


@app.route('/report')
def report():
    # Fetch existing and new metrics
    total_customers = fetch_total_customers()
    total_bookings = fetch_total_bookings()
    movies_available = fetch_movies_available()
    recent_customers = fetch_recent_customers(limit=5)
    bookings_per_month = fetch_bookings_per_month()
    total_revenue = fetch_total_revenue()

    # New metrics
    peak_revenue_days = fetch_peak_revenue_days(limit=5)
    most_popular_movies = fetch_most_popular_movies(limit=5)
    hall_utilization = fetch_hall_utilization_rate()
    revenue_per_genre = fetch_revenue_per_genre()

    # Render template
    return render_template(
        'report.html',
        total_customers=total_customers,
        total_bookings=total_bookings,
        movies_available=movies_available,
        recent_customers=recent_customers,
        bookings_per_month=bookings_per_month,
        total_revenue=total_revenue,
        peak_revenue_days=peak_revenue_days,
        most_popular_movies=most_popular_movies,
        hall_utilization=hall_utilization,
        revenue_per_genre=revenue_per_genre
    )
@app.route('/customer_bookings')
def customer_bookings():
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        
        query = """
        SELECT 
            t.TicketID,
            c.customer_name AS CustomerName,
            c.customer_phone AS CustomerPhone,
            m.MovieName,
            ms.ShowDate,
            ms.ShowTime,
            h.Hall_name AS HallName,
            s.Seat_Row AS SeatRow,
            s.Seat_Column AS SeatColumn,
            m.Price AS MoviePrice
        FROM 
            Ticket t
        JOIN 
            Customer c ON t.CustomerID = c.customer_id
        JOIN 
            movie_show ms ON t.ShowID = ms.ShowID
        JOIN 
            movie m ON ms.MovieID = m.MovieID
        JOIN 
            Hall h ON ms.HallID = h.Hall_ID
        JOIN 
            hall_seat hs ON t.SeatID = hs.SeatID
        JOIN 
            seat s ON hs.SeatID = s.Seat_id
        """
        
        cursor.execute(query)
        bookings = cursor.fetchall()
        
        cursor.close()
        connection.close()
        
        return render_template('customer_bookings.html', bookings=bookings)
    except Exception as e:
        return f"An error occurred: {e}", 500
    
@app.route('/CashierLog', methods=['GET', 'POST'])
def cashier_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        try:
            # Connect to the database
            connection = get_db_connection()
            cursor = connection.cursor(dictionary=True)
            
            # Query the cashier table to check credentials
            query = """
            SELECT * FROM Cashier 
            WHERE cashier_name = %s AND cashier_password = %s
            """
            cursor.execute(query, (username, password))
            cashier = cursor.fetchone()
            
            if cashier:
                # Set session or flash message for success
                session['cashier_id'] = cashier['Employee_id']
                flash('Login successful!', 'success')
                return redirect('/cashier/dashboard')  # Replace with your cashier dashboard route
            else:
                flash('Invalid username or password', 'danger')
        except Exception as e:
            flash(f"An error occurred: {e}", 'danger')
        finally:
            cursor.close()
            connection.close()
    
    return render_template('CashierLog.html')

@app.route('/manage_food')
def cashier_dashboard():
    if 'cashier_id' not in session:
        flash('Please log in to access this page.', 'danger')
        return redirect('/CashierLog')
    
    return render_template('CashierLog.html')  # Replace with your actual dashboard template



@app.route('/manage_food', methods=['GET', 'POST'])
def manage_food():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    if request.method == 'POST':
        action = request.form.get('action')

        try:
            if action == 'add':
                # Add a new item
                item_name = request.form['item_name']
                quantity = int(request.form['quantity'])
                price = float(request.form['price'])
                cursor.execute(
                    "INSERT INTO Food_item (Item_name, Quantity_Available, Price) VALUES (%s, %s, %s)",
                    (item_name, quantity, price)
                )
                connection.commit()
                flash("Food item added successfully!", "success")
            elif action == 'delete':
                # Delete an item
                item_id = int(request.form['item_id'])
                cursor.execute("DELETE FROM Food_item WHERE item_id = %s", (item_id,))
                connection.commit()
                flash("Food item deleted successfully!", "success")
            elif action == 'update':
                # Update an existing item
                item_id = int(request.form['item_id'])
                item_name = request.form.get('item_name')
                quantity = request.form.get('quantity')
                price = request.form.get('price')

                # Build the dynamic query for update
                query = "UPDATE Food_item SET "
                params = []

                if item_name:
                    query += "Item_name = %s, "
                    params.append(item_name)
                if quantity:
                    query += "Quantity_Available = %s, "
                    params.append(quantity)
                if price:
                    query += "Price = %s, "
                    params.append(price)

                # Remove the trailing comma
                query = query.rstrip(", ")
                query += " WHERE item_id = %s"
                params.append(item_id)

                cursor.execute(query, tuple(params))
                connection.commit()
                flash("Food item updated successfully!", "success")
        except Exception as e:
            flash(f"An error occurred: {e}", "danger")

    # Fetch food items for the table
    search_query = request.args.get('search', '')
    query = "SELECT * FROM Food_item WHERE Item_name LIKE %s"
    cursor.execute(query, (f"%{search_query}%",))
    food_items = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template('food_item.html', food_items=food_items, search_query=search_query)

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    if request.method == 'POST':
        action = request.form.get('action')
        try:
            if action == 'add':
                item_name = request.form['item_name']
                quantity = int(request.form['quantity'])
                price = float(request.form['price'])
                cursor.execute(
                    """
                    INSERT INTO Food_item (Item_name, Quantity_Available, Price)
                    VALUES (%s, %s, %s)
                    """, (item_name, quantity, price)
                )
                connection.commit()
                flash("Food item added successfully!", "success")
            elif action == 'update':
                item_id = int(request.form['item_id'])
                item_name = request.form['item_name']
                quantity = int(request.form['quantity'])
                price = float(request.form['price'])
                cursor.execute(
                    """
                    UPDATE Food_item
                    SET Item_name = %s, Quantity_Available = %s, Price = %s
                    WHERE item_id = %s
                    """, (item_name, quantity, price, item_id)
                )
                connection.commit()
                flash("Food item updated successfully!", "success")
            elif action == 'delete':
                item_id = int(request.form['item_id'])
                cursor.execute("DELETE FROM Food_item WHERE item_id = %s", (item_id,))
                connection.commit()
                flash("Food item deleted successfully!", "success")
        except Exception as e:
            flash(f"An error occurred: {e}", "danger")
    
    # Fetch food items
    search_query = request.args.get('search', '')
    query = "SELECT * FROM Food_item WHERE Item_name LIKE %s"
    cursor.execute(query, (f"%{search_query}%",))
    food_items = cursor.fetchall()
    
    cursor.close()
    connection.close()
    
    return render_template('food_item.html', food_items=food_items, search_query=search_query)

@app.route('/food_item', methods=['GET', 'POST'])
def manage_food_items():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    if request.method == 'POST':
        # Handle form submission for adding or deleting food items
        item_name = request.form.get('item_name')
        action = request.form.get('action')
        
        if action == 'add':
            try:
                query = "INSERT INTO Food_item (Item_name, Quantity_Available, Price) VALUES (%s, %s, %s)"
                cursor.execute(query, (item_name, request.form['quantity'], request.form['price']))
                connection.commit()
                flash("Food item added successfully!", "success")
            except Exception as e:
                flash(f"An error occurred: {e}", "danger")
        elif action == 'delete':
            try:
                query = "DELETE FROM Food_item WHERE Item_name = %s"
                cursor.execute(query, (item_name,))
                connection.commit()
                flash("Food item deleted successfully!", "success")
            except Exception as e:
                flash(f"An error occurred: {e}", "danger")
    
    # Fetch all items
    query = "SELECT * FROM Food_item"
    cursor.execute(query)
    food_items = cursor.fetchall()

    # Fetch search results
    search_query = request.args.get('search', '')
    column = request.args.get('column', '')
    search_results = []
    if column and search_query:
        # Validate column name
        valid_columns = ['item_id', 'Item_name', 'Quantity_Available', 'Price']
        if column in valid_columns:
            try:
                # Use `=` for exact matches if column is `item_id` or `Quantity_Available`
                if column in ['item_id', 'Quantity_Available']:
                    search_query_sql = f"SELECT * FROM Food_item WHERE {column} = %s"
                    cursor.execute(search_query_sql, (search_query,))
                else:
                    # Use `LIKE` for string columns
                    search_query_sql = f"SELECT * FROM Food_item WHERE {column} LIKE %s"
                    cursor.execute(search_query_sql, (f"%{search_query}%",))
                search_results = cursor.fetchall()
            except Exception as e:
                flash(f"An error occurred while searching: {e}", "danger")

    cursor.close()
    connection.close()

    return render_template(
        'food_item.html',
        food_items=food_items,
        search_results=search_results,
        search_query=search_query,
        column=column
    )

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    if request.method == 'POST':
        # Handle form submission for adding or deleting food items
        item_name = request.form.get('item_name')
        action = request.form.get('action')
        
        if action == 'add':
            try:
                query = "INSERT INTO Food_item (Item_name, Quantity_Available, Price) VALUES (%s, %s, %s)"
                cursor.execute(query, (item_name, request.form['quantity'], request.form['price']))
                connection.commit()
                flash("Food item added successfully!", "success")
            except Exception as e:
                flash(f"An error occurred: {e}", "danger")
        elif action == 'delete':
            try:
                query = "DELETE FROM Food_item WHERE Item_name = %s"
                cursor.execute(query, (item_name,))
                connection.commit()
                flash("Food item deleted successfully!", "success")
            except Exception as e:
                flash(f"An error occurred: {e}", "danger")
    
    # Fetch all items
    query = "SELECT * FROM Food_item"
    cursor.execute(query)
    food_items = cursor.fetchall()

    # Fetch search results
    search_query = request.args.get('search', '')
    column = request.args.get('column', '')
    search_results = []
    if column and search_query:
        # Validate column name
        valid_columns = ['item_id', 'Item_name', 'Quantity_Available', 'Price']
        if column in valid_columns:
            try:
                search_query_sql = f"SELECT * FROM Food_item WHERE {column} LIKE %s"
                cursor.execute(search_query_sql, (f"%{search_query}%",))
                search_results = cursor.fetchall()
            except Exception as e:
                flash(f"An error occurred while searching: {e}", "danger")

    cursor.close()
    connection.close()

    return render_template(
        'food_item.html',
        food_items=food_items,
        search_results=search_results,
        search_query=search_query,
        column=column
    )

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    if request.method == 'POST':
        # Handle form submission for adding or deleting food items
        item_name = request.form.get('item_name')
        action = request.form.get('action')
        
        if action == 'add':
            try:
                query = "INSERT INTO Food_item (Item_name, Quantity_Available, Price) VALUES (%s, %s, %s)"
                cursor.execute(query, (item_name, request.form['quantity'], request.form['price']))
                connection.commit()
                flash("Food item added successfully!", "success")
            except Exception as e:
                flash(f"An error occurred: {e}", "danger")
        elif action == 'delete':
            try:
                query = "DELETE FROM Food_item WHERE Item_name = %s"
                cursor.execute(query, (item_name,))
                connection.commit()
                flash("Food item deleted successfully!", "success")
            except Exception as e:
                flash(f"An error occurred: {e}", "danger")
    
    # Handle GET requests and search functionality
    view = request.args.get('view', 'all')
    search_query = request.args.get('search', '')
    column = request.args.get('column', '')
    items_to_display = []

    if view == 'search' and column and search_query:
        # Validate column name
        valid_columns = ['item_id', 'Item_name', 'Quantity_Available', 'Price']
        if column in valid_columns:
            try:
                search_query_sql = f"SELECT * FROM Food_item WHERE {column} LIKE %s"
                cursor.execute(search_query_sql, (f"%{search_query}%",))
                items_to_display = cursor.fetchall()
            except Exception as e:
                flash(f"An error occurred while searching: {e}", "danger")
        else:
            flash("Invalid column for search.", "danger")
    else:
        # Fetch all items if no search
        query = "SELECT * FROM Food_item"
        cursor.execute(query)
        items_to_display = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        'food_item.html',
        items_to_display=items_to_display,
        search_query=search_query,
        column=column,
        view=view
    )

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    # Fetch search results if 'view=search' is specified
    view = request.args.get('view', 'all')
    search_query = request.args.get('search', '')
    column = request.args.get('column', '')

    items_to_display = []

    if view == 'search' and column and search_query:
        # Validate column name
        valid_columns = ['item_id', 'Item_name', 'Quantity_Available', 'Price']
        if column in valid_columns:
            try:
                search_query_sql = f"SELECT * FROM Food_item WHERE {column} LIKE %s"
                cursor.execute(search_query_sql, (f"%{search_query}%",))
                items_to_display = cursor.fetchall()
            except Exception as e:
                flash(f"An error occurred while searching: {e}", "danger")
        else:
            flash("Invalid column for search.", "danger")
    else:
        # Fetch all items if no search
        query = "SELECT * FROM Food_item"
        cursor.execute(query)
        items_to_display = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        'food_item.html',
        items_to_display=items_to_display,
        search_query=search_query,
        column=column,
        view=view
    )

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    if request.method == 'POST':
        # Handle form submission for adding or deleting food items
        item_name = request.form.get('item_name')
        action = request.form.get('action')
        
        if action == 'add':
            try:
                query = "INSERT INTO Food_item (Item_name, Quantity_Available, Price) VALUES (%s, %s, %s)"
                cursor.execute(query, (item_name, request.form['quantity'], request.form['price']))
                connection.commit()
                flash("Food item added successfully!", "success")
            except Exception as e:
                flash(f"An error occurred: {e}", "danger")
        elif action == 'delete':
            try:
                query = "DELETE FROM Food_item WHERE Item_name = %s"
                cursor.execute(query, (item_name,))
                connection.commit()
                flash("Food item deleted successfully!", "success")
            except Exception as e:
                flash(f"An error occurred: {e}", "danger")
    
    # Fetch all items
    query = "SELECT * FROM Food_item"
    cursor.execute(query)
    food_items = cursor.fetchall()

    # Fetch search results
    search_query = request.args.get('search', '')
    column = request.args.get('column', '')
    search_results = []
    if column and search_query:
        # Prevent SQL injection by validating column name
        valid_columns = ['item_id', 'Item_name', 'Quantity_Available', 'Price']
        if column in valid_columns:
            search_query_sql = f"SELECT * FROM Food_item WHERE {column} LIKE %s"
            cursor.execute(search_query_sql, (f"%{search_query}%",))
            search_results = cursor.fetchall()
        else:
            flash("Invalid column for search.", "danger")

    cursor.close()
    connection.close()

    # Determine which list to display based on the 'view' parameter
    view = request.args.get('view', 'all')
    if view == 'search':
        items_to_display = search_results
    else:
        items_to_display = food_items

    return render_template(
        'food_item.html',
        items_to_display=items_to_display,
        food_items=food_items,
        search_results=search_results,
        search_query=search_query,
        column=column,
        view=view
    )

@app.route('/food-court')
def food_court():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    # Fetch food items
    cursor.execute("SELECT * FROM Food_item")
    food_items = cursor.fetchall()
    
    connection.close()
    return render_template('food-court.html', food_items=food_items)


@app.route('/edit_food_item', methods=['POST'])
def edit_food_item():
    # Connect to the database
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        # Get form data
        item_id = request.form.get('item_id')  # Required
        item_name = request.form.get('item_name')  # Optional
        quantity = request.form.get('quantity')  # Optional
        price = request.form.get('price')  # Optional

        # Ensure Item ID is provided
        if not item_id:
            flash("Item ID is required to edit a food item.", "danger")
            return redirect('/food_item')

        # Build dynamic SQL query based on provided fields
        query = "UPDATE Food_item SET "
        params = []

        if item_name:
            query += "Item_name = %s, "
            params.append(item_name)
        if quantity:
            query += "Quantity_Available = %s, "
            params.append(quantity)
        if price:
            query += "Price = %s, "
            params.append(price)

        # Remove the trailing comma and add the WHERE clause
        query = query.rstrip(", ") + " WHERE item_id = %s"
        params.append(item_id)

        # Execute the query only if there are fields to update
        if len(params) > 1:  # At least one field + item_id
            cursor.execute(query, tuple(params))
            connection.commit()
            flash("Food item updated successfully!", "success")
        else:
            flash("No fields provided for update.", "warning")

    except Exception as e:
        flash(f"An error occurred: {e}", "danger")
    finally:
        cursor.close()
        connection.close()

    return redirect('/food_item')


@app.route('/man', methods=['GET'])
def man():
    # Sorting parameters
    sort_by = request.args.get('sort_by', 'item_id')  # Default column
    order = request.args.get('order', 'asc')  # Default order

    # Validate sorting parameters to prevent SQL injection
    valid_columns = ['item_id', 'Item_name', 'Quantity_Available', 'Price']
    if sort_by not in valid_columns:
        sort_by = 'item_id'
    if order not in ['asc', 'desc']:
        order = 'asc'

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    # Fetch sorted data
    query = f"SELECT * FROM Food_item ORDER BY {sort_by} {order}"
    cursor.execute(query)
    food_items = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        'food_item.html',
        food_items=food_items,
        sort_by=sort_by,
        order=order
    )


if __name__ == "__main__":
    app.run(debug=True)
