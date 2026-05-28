from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os
import re

load_dotenv()

app = Flask(__name__)

app.config.update(
    MAIL_SERVER=os.getenv("MAIL_SERVER"),
    MAIL_PORT=int(os.getenv("MAIL_PORT", 587)),
    MAIL_USE_TLS=os.getenv("MAIL_USE_TLS") == "True",
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
)

app.secret_key = os.getenv("SECRET_KEY")

mail = Mail(app)

def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/contact', methods=['POST'])
def contact():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')

    if not (name and email and message):
        flash("All fields are required.", category="error")
        return redirect(url_for('home'))

    if not is_valid_email(email):
        flash("Invalid email address.", category="error")
        return redirect(url_for('home'))

    msg = Message(
        subject=f"New Contact from {name}",
        sender=os.getenv("MAIL_USERNAME"),      # prodge1293@gmail.com
        reply_to=email,                          # visitor's email
        recipients=[os.getenv("MAIL_USERNAME")]  # sending to yourself
    )
    msg.body = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"

    try:
        mail.send(msg)
        session['form_submitted'] = True
        flash("Message sent successfully!", category="success")
        return redirect(url_for('success'))
    except Exception as e:
        print(f"Mail error: {e}")
        flash("Error sending message. Please try again later.", category="error")
        return redirect(url_for('home'))

@app.route('/success')
def success():
    if not session.get('form_submitted'):
        return redirect(url_for('home'))
    session.pop('form_submitted')
    return render_template('success.html')

if __name__ == "__main__":
    app.run(debug=True)