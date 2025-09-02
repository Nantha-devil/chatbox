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

    # Medical chatbot using if-else conditions
    if msg in ['hi', 'hello']:
        reply = 'Hello! I am your medical assistant bot. Ask me about any disease.'
    elif msg == 'how are you':
        reply = 'I am just a bot, but I am ready to help with medical info!'
    elif msg == 'bye':
        reply = 'Goodbye! Take care of your health!'

    # Example diseases
    elif msg == 'diabetes':
        reply = ("Diabetes is a chronic disease that occurs when the body cannot "
                 "produce enough insulin or use it effectively.\n"
                 "👉 Symptoms: frequent urination, thirst, fatigue, blurred vision.\n"
                 "👉 Treatment: insulin, oral medications, lifestyle changes.\n"
                 "👉 Prevention: healthy diet, regular exercise, weight control.")
    elif msg == 'asthma':
        reply = ("Asthma is a condition in which your airways narrow and swell.\n"
                 "👉 Symptoms: coughing, wheezing, shortness of breath.\n"
                 "👉 Treatment: inhalers, bronchodilators, corticosteroids.\n"
                 "👉 Prevention: avoid allergens, pollution, and cold air.")
    elif msg == 'covid' or msg == 'covid-19' or msg == 'corona':
        reply = ("COVID-19 is a viral infection caused by SARS-CoV-2.\n"
                 "👉 Symptoms: fever, cough, loss of smell/taste, fatigue.\n"
                 "👉 Treatment: rest, fluids, antiviral medicines (if prescribed).\n"
                 "👉 Prevention: vaccination, masks, social distancing.")
    elif msg == 'malaria':
        reply = ("Malaria is a mosquito-borne infectious disease.\n"
                 "👉 Symptoms: fever, chills, headache, sweating.\n"
                 "👉 Treatment: antimalarial drugs.\n"
                 "👉 Prevention: mosquito nets, repellents, clean environment.")
    elif msg == 'hypertension' or msg == 'high blood pressure':
        reply = ("Hypertension means consistently high blood pressure.\n"
                 "👉 Symptoms: often none, sometimes headaches, dizziness.\n"
                 "👉 Treatment: lifestyle changes, antihypertensive medicines.\n"
                 "👉 Prevention: low-salt diet, exercise, stress management.")

    # Fallback
    else:
        reply = "I don't have information about that. Please try asking about a disease name."

    # Save chat to DB
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