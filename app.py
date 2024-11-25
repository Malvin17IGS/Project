from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'pemenang_db'
}

# Halaman utama
@app.route('/')
def home():
    return render_template('login.html')

# Halaman registrasi
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        conn.commit()
        cursor.close()
        conn.close()
        
        flash('Registrasi berhasil! Silakan masuk.', 'success')
        return redirect(url_for('home'))
    
    return render_template('register.html')

# Halaman login
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if user and check_password_hash(user[2], password):
        session['user_id'] = user[0]
        session['username'] = user[1]
        return redirect(url_for('winners'))
    
    flash('Username atau password salah!', 'danger')
    return redirect(url_for('home'))

# Halaman daftar pemenang
@app.route('/winners')
def winners():
    if 'user_id' not in session:
        return redirect(url_for('home'))
    
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM winners")
    winners = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return render_template('winners.html', winners=winners)

# Halaman logout
@app.route('/logout')
def logout():
    session.clear()
    flash('Anda telah keluar.', 'success')
    return redirect(url_for('home'))

@app.route('/introduction')
def introduction():
    return render_template("introduction.html")

@app.route('/beranda')
def beranda():
    return render_template("home.html")

if __name__ == '__main__':
    app.run(debug=True)