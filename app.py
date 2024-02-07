from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3  # Make sure to import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash  # Import necessary functions
from led_control import set_color, clear_strip

app = Flask(__name__)
app.secret_key = 'ciocolata'  # It's good to define the secret key at the beginning

# Database related functions
def get_db_connection():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn

def create_user(username, password):
    conn = get_db_connection()
    conn.execute('INSERT INTO users (username, password) VALUES (?, ?)',
                 (username, password))
    conn.commit()
    conn.close()

def get_user(username):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    conn.close()
    return user

# Route definitions
@app.route('/')
def index():
    # Check if user is logged in
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    if 'username' in session:  # Check if the user is logged in
        return render_template('dashboard.html')  # Render the dashboard template
    return redirect(url_for('index'))  # If not logged in, redirect to the login page

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = get_user(username)
        if user and check_password_hash(user['password'], password):
            session['username'] = username
            return redirect(url_for('dashboard'))

        # If user is not authenticated, reload login page
        return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Hash the password
        hashed_password = generate_password_hash(password)

        create_user(username, hashed_password)
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/logout')
def logout():
    # Removing username from session
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/led/on')
def led_on():
    set_color(255, 0, 0)  # Set to red, change as needed
    return redirect(url_for('dashboard'))

@app.route('/led/off')
def led_off():
    clear_strip()
    return redirect(url_for('dashboard'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

