import ssl
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from tgbot.config import load_config
from email.mime.multipart import MIMEMultipart


async def send_mail(receiver: str, username: str):

    config = load_config('.env')
    server = config.mail.server
    sender_email = config.mail.mail_acc
    password = config.mail.password

    subject = "An email with QR Code fro freeipa auth"
    body = "This is an email with qr code file, you need to scan this picture and use it for auth"
    receiver_email = receiver

    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message["Bcc"] = receiver_email  # Recommended for mass emails

    # Add body to email
    message.attach(MIMEText(body, "plain"))
    filename = f'{config.misc.qr_code_path}/{username}.png'  # In same directory as script

    # Open PDF file in binary mode
    with open(filename, "rb") as attachment:
        # Add file as application/octet-stream
        # Email client can usually download this automatically as attachment
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

        # Encode file in ASCII characters to send by email
    encoders.encode_base64(part)

    # Add header as key/value pair to attachment part
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {filename}",
        )

    # Add attachment to message and convert message to string
    message.attach(part)
    text = message.as_string()

    # Log in to server using secure context and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(host=server, context=context) as send:
        send.login(sender_email, password)
        send.sendmail(sender_email, receiver_email, text)
