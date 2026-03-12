from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mail import Mail, Message

app = Flask(__name__)
app.secret_key = "supersecretkey"  # for flash messages

# Configure Flask-Mail
app.config.update(
    MAIL_SERVER="smtp.gmail.com",
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USERNAME="prodge1293@gmail.com",  # replace with your email
    MAIL_PASSWORD="mkft kzig fxwb xgsd"       # use an app password for Gmail
)

mail = Mail(app)

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

    msg = Message(f"New Contact from {name}",
                  sender=email,
                  recipients=['your.email@gmail.com'])
    msg.body = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"

    try:
        mail.send(msg)
        flash("Message sent successfully!", category="success")
        return redirect(url_for('success'))
    except Exception as e:
        flash("Error sending message. Please try again later.", category="error")
        return redirect(url_for('home'))

@app.route('/success')
def success():
    return render_template('success.html')

if __name__ == "__main__":
    app.run(debug=True)
