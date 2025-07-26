import smtplib
import ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import threading

send_event = threading.Event()
detection_info = None

# Setup email server
subject = "Weapon Detection Alert"
sender_email = "mail.server.tech@gmail.com"
receiver_email = "muhammad.alifbabu@gmail.com"
password = "tuns rrbt xpio gjmx"

def set_detection_info(age, gender, expression):
    global detection_info
    detection_info = {'age': age, 'gender': gender, 'expression': expression}

def send_mail():
    while True:
        send_event.wait()
        send_event.clear()

        # Create a multipart message and set headers
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject
        message["Bcc"] = receiver_email

        # Create email body with detection information
        global detection_info
        if detection_info:
            body = f"""A weapon has been detected in the surveillance footage.
Detection Details:
- Age: {detection_info['age']}
- Gender: {detection_info['gender']}
- Expression: {detection_info['expression']}
"""
        else:
            body = "A weapon has been detected in the surveillance footage."

        # Add body to email
        message.attach(MIMEText(body, "plain"))

        filename = 'cell phone.png'

        try:
            # Open image file in binary mode
            with open(filename, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())

            # Encode file in ASCII characters
            encoders.encode_base64(part)

            # Add header to attachment part
            part.add_header(
                "Content-Disposition",
                f"attachment; filename= {filename}",
            )

            # Add attachment to message
            message.attach(part)
            text = message.as_string()

            # Log in to server using secure context and send email
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_email, text)
            print("Email sent successfully")
        except Exception as e:
            print(f"Email could not be sent. Error: {str(e)}")