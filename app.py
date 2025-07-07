from flask import Flask, render_template, request, redirect, url_for, session, send_file
import mysql.connector
import pandas as pd
import io
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MySQL connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="chatbotdb"
)
cursor = db.cursor(dictionary=True)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        uname = request.form['username']
        pwd = request.form['password']
        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (uname, pwd))
        user = cursor.fetchone()
        if user:
            session['user_id'] = user['id']
            return redirect('/chat')
        else:
            return "Invalid credentials"
    return render_template('login.html')

@app.route('/chat')
def chat():
    if 'user_id' not in session:
        return redirect('/')
    return render_template('chat.html')

@app.route('/send', methods=['POST'])
def send():
    if 'user_id' not in session:
        return 'Unauthorized', 401
    msg = request.form['message'].lower()

    # Simple rule-based replies using if statements
    if msg == 'hi' or msg == 'hello':
        reply = 'Hello! How can I help you today?'
    elif msg == 'how are you':
        reply = 'I am just a bot, but I am doing fine. Thanks for asking!'
    elif msg == 'bye':
        reply = 'Goodbye! Have a great day!'
    elif 'your name' in msg:
        reply = 'I am your friendly chatbot.'
    else:
        reply = "I'm not sure how to respond to that."

    cursor.execute("INSERT INTO chats (user_id, message, reply) VALUES (%s, %s, %s)",
                (session['user_id'], msg, reply))
    db.commit()
    return reply


@app.route('/history')
def history():
    if 'user_id' not in session:
        return redirect('/')
    cursor.execute("SELECT * FROM chats WHERE user_id=%s ORDER BY timestamp", (session['user_id'],))
    chats = cursor.fetchall()
    return {'chats': chats}

# Admin Login
@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'admin123':
            session['admin'] = True
            return redirect('/admin-dashboard')
        else:
            return "Invalid admin credentials"
    return render_template('admin_login.html')

@app.route('/admin-dashboard')
def admin_dashboard():
    if not session.get('admin'):
        return redirect('/admin')
    cursor.execute("""
        SELECT u.username, c.message, c.reply, c.timestamp 
        FROM chats c 
        JOIN users u ON c.user_id = u.id 
        ORDER BY c.timestamp DESC
    """)
    data = cursor.fetchall()
    return render_template('admin_dashboard.html', chats=data)

@app.route('/admin-logout')
def admin_logout():
    session.pop('admin', None)
    return redirect('/admin')

@app.route('/export-chats')
def export_chats():
    if not session.get('admin'):
        return redirect('/admin')
    cursor.execute("""
        SELECT u.username, c.message, c.reply, c.timestamp 
        FROM chats c 
        JOIN users u ON c.user_id = u.id 
        ORDER BY c.timestamp DESC
    """)
    data = cursor.fetchall()
    df = pd.DataFrame(data)
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Chats', index=False)
    output.seek(0)
    return send_file(output, download_name="chat_logs.xlsx", as_attachment=True)

@app.route('/clear')
def clear():
    session['conversation'] = []
    return redirect(url_for('chat'))


@app.route('/', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        uname = request.form['username']
        email = request.form['email']
        pwd = request.form['password']
        dob = request.form['dob']
        
        # Optional: prevent duplicate usernames
        cursor.execute("SELECT * FROM users WHERE username=%s", (uname,))
        if cursor.fetchone():
            return "Username already exists"

        cursor.execute("INSERT INTO users (username, email, password, dob) VALUES (%s, %s, %s, %s)",
                       (uname, email, pwd, dob))
        db.commit()
        return redirect('/chat')
    return render_template('signup.html')


if __name__ == '__main__':
    app.run(debug=True)
