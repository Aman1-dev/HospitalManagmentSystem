import json
import smtplib
import os

from email.mime.text import MIMEText


def send(event, context):

    body = json.loads(event["body"])

    receiver = body["email"]
    subject = body["subject"]
    message = body["message"]

    sender = os.environ["EMAIL"]
    password = os.environ["APP_PASSWORD"]

    msg = MIMEText(message)
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = receiver

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender, password)
    server.sendmail(sender, receiver, msg.as_string())
    server.quit()

    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "message": "Email sent successfully"
            }
        )
    }