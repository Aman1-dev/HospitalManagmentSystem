from flask import Flask, request, jsonify
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)


@app.route("/send-email", methods=["POST"])
def send_email():

    data = request.json

    receiver = data["email"]
    subject = data["subject"]
    message = data["message"]

    sender = "moryaaman06@gmail.com"
    password = "Amankumar_26165537"

    msg = MIMEText(message)
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = receiver

    server = smtplib.SMTP("smtp.gmail.com", 587)

    server.starttls()

    server.login(sender, password)

    server.sendmail(sender, receiver, msg.as_string())

    server.quit()

    return jsonify(
        {
            "message": "Email Sent"
        }
    )


if __name__ == "__main__":
    app.run(port=5000)