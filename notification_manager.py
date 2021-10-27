import smtplib
from email.message import EmailMessage

SMTP_ADDRESSES = {
    "gmail": "smtp.gmail.com",
    "hotmail": "smtp.live.com",
    "outlook": "outlook.office365.com",
    "yahoo": "smtp.mail.yahoo.com"
}
GMAIL_PORT = 587


class NotificationManager:

    def __init__(self, email, password):
        self.email = email
        self.email_provider = self.email.split('@')[1].split('.')[0]
        self.smtp_address = SMTP_ADDRESSES[self.email_provider]
        self.password = password

    def __make_msg(self, to_email, message_text):
        msg = EmailMessage()
        msg.set_content(message_text)
        msg["Subject"] = "Flight Finder found a flight"
        msg["From"] = self.email
        msg["To"] = to_email
        msg["Bcc"] = to_email
        return msg

    def send_email(self, to_email, message_text):
        message = self.__make_msg(to_email, message_text)
        if self.email_provider == "gmail":
            connection = smtplib.SMTP(self.smtp_address, port=GMAIL_PORT)
        else:
            connection = smtplib.SMTP(self.smtp_address)
        connection.starttls()
        connection.login(user=self.email, password=self.password)
        connection.send_message(message)
        connection.close()
