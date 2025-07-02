from flask import Flask, render_template, request, session, redirect, url_for
import mysql.connector
app = Flask(__name__)
app.secret_key = 'your_secret_key'

 #save the database
db=mysql.connector.connect(host='localhost',user='root',password='',database='chatbox')
cursor=db.cursor()

def get_response(user_input):
    user_input = user_input.lower()

    if "headache" in user_input:
        return "🤕 Drink water and rest. If it persists, consult a doctor."
    elif "fever" in user_input:
        return "🌡️ Take paracetamol and stay hydrated."
    elif "cold" in user_input or "cough" in user_input:
        return "🤧 Drink warm fluids and rest well."
    elif "sore throat" in user_input:
        return "🗣️ Gargle with warm salt water."
    elif "stomach pain" in user_input:
        return "🤢 Eat light and avoid spicy food."
    elif "diabetes" in user_input:
        return "🩸 Follow a low-sugar diet and check sugar regularly."
    elif "bp" in user_input or "blood pressure" in user_input:
        return "💓 Avoid salty food and monitor your BP."
    elif "exercise" in user_input:
        return "🏃 Do 30 minutes of activity daily."
    elif "diet" in user_input:
        return "🥗 Eat balanced meals with fruits and veggies."
    elif "sleep" in user_input:
        return "😴 Get 7-8 hours of quality sleep."
    elif "stress" in user_input:
        return "🧘 Try breathing exercises or yoga."
    elif "skin" in user_input:
        return "🧴 Stay hydrated and use moisturizers."
    elif "hair" in user_input:
        return "💇 Oil your hair and avoid heat tools."
    elif "eyes" in user_input:
        return "👀 Take screen breaks and blink often."
    elif "hydration" in user_input:
        return "💧 Drink at least 8 glasses of water."
    elif "vitamin d" in user_input:
        return "☀️ Get morning sunlight and eat dairy."
    elif "weight loss" in user_input:
        return "⚖️ Avoid junk food and stay active."
    elif "covid" in user_input:
        return "😷 Wear a mask and wash hands."
    elif "heart" in user_input:
        return "❤️ Avoid fried foods and get regular checks."
    elif "pregnancy" in user_input:
        return "🤰 Eat healthy and follow your doctor’s advice."

    else:
        return "❓ Sorry, I don't have a tip for that. Try asking about fever, stress, or hydration."

@app.route('/', methods=['GET', 'POST'])
def chat():
    # Reset conversation on page load
    while True:
        if request.method == 'GET':
            session['conversation'] = []

        if 'conversation' not in session:
            session['conversation'] = []

        if request.method == 'POST':
            user_input = request.form['user_input']
            bot_response = get_response(user_input)
            session['conversation'].append(("🧑 You", user_input))
            session['conversation'].append(("🤖 Bot", bot_response))
            session.modified = True

            cursor.execute("INSERT INTO chat(user,message)VALUES(%s,%s)",('🧑 You',user_input))
            cursor.execute("INSERT INTO chat(user,message)VALUES(%s,%s)",("🤖 Bot", bot_response))
            db.commit()
            cursor.close()
            db.close()
        

        return render_template('chat.html', conversation=session['conversation'])
    


@app.route('/clear')
def clear():
    session['conversation'] = []
    return redirect(url_for('chat'))

if __name__ == '__main__':
    app.run(debug=True)
