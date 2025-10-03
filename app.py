
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from mysql.connector import MySQLConnection, Error

app = Flask(__name__)
app.secret_key = 'mykey'  # Required for flash messages

def create_connection():
    """Creates a database connection."""
    try:
        connection = MySQLConnection(
            host="localhost",
            database="talent_edge",
            user="root",
            password="root@123"
        )
        print("Connection to MySQL DB successful")
        return connection
    except Error as e:
        print(f"Database connection error: {e}")
        return None

@app.route('/')
def home():
    return render_template('index.html')  # Ensure 'index.html' is in the 'templates' folder

@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/about.html')
def about():
    return render_template('about.html')

@app.route('/blog.html')
def blog():
    return render_template('blog.html')

@app.route('/contact.html')
def contact():
    return render_template('contact.html')


@app.route('/faq.html')
def faq():
    return render_template('faq.html')

@app.route('/gallery.html')
def gallery():
    return render_template('gallery.html')

@app.route('/main.html')
def main():
    return render_template('main.html')

@app.route('/portfolio-single.html')
def portfoliosingle():
    return render_template('portfolio-single.html')

@app.route('/portfolio.html')
def portfolio():
    return render_template('portfolio.html')

@app.route('/service-single.html')
def servicesingle():
    return render_template('service-single.html')

@app.route('/services.html')
def services():
    return render_template('services.html')

@app.route('/testimonials.html')
def testimonials():
    return render_template('testimonials.html')

@app.route('/blog-single.html')
def blogsingle():
    return render_template('blog-single.html')

@app.route('/register.html', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get form data
        fullname = request.form.get('fullname')
        email = request.form.get('email')
        experience = request.form.get('experience')
        qualification = request.form.get('qualification')
        phone = request.form.get('phone')
        role = request.form.get('role')
        interest = request.form.get('interest')

        # Database operation
        connection = create_connection()
        if connection:
            try:
                with connection.cursor() as cursor:
                    cursor.execute("""
                        INSERT INTO users (fullname, email, experience, qualification, phone, role, interest)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """, (fullname, email, experience, qualification, phone, role, interest))
                    connection.commit()
                    flash('Registration successful!', 'success')
                    return redirect(url_for('home'))
            except Error as e:
                print(f"Database operation error: {e}")
                flash('Registration failed. Please try again.', 'danger')
                return jsonify({'error': 'Database operation error', 'message': str(e)})
            finally:
                connection.close()
        else:
            flash('Unable to connect to the database. Please try later.', 'danger')
            return jsonify({'error': 'Database connection error'})

    return render_template('register.html')

app.secret_key = 'siva'  # Required for session management

# Fixed email and password
FIXED_EMAIL = "admin123@gmail.com"
FIXED_PASSWORD = "admin@123"


@app.route('/login.html', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Check if the email and password match the fixed values
        if email == FIXED_EMAIL and password == FIXED_PASSWORD:
            return redirect(url_for('users'))  # Redirect to index page
        else:
            flash('Invalid email or password. Please try again.', 'danger')

    return render_template('login.html')  # Render your login page
@app.route('/view_users.html')
def view_users():
    connection = create_connection()
    users = []
    if connection:
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM users")  # Fetch all users
                users = cursor.fetchall()  # Get all results
        except Error as e:
            print(f"Database operation error: {e}")
            flash('Unable to fetch user data.', 'danger')
        finally:
            connection.close()
    return render_template('view_users.html', users=users)  # Pass users to the template

if __name__ == '__main__':
    (app.run(debug=True))
    


