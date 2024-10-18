import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from dotenv import load_dotenv

# Load environment variables from .env file
class Sender:
    def __init__(self):
        load_dotenv()
        self.EMAIL_APP_ACCOUNT = os.getenv("EMAIL_APP_ACCOUNT")
        self.EMAIL_APP_PASSWORD = os.getenv("EMAIL_APP_PASSWORD")

    def send_custom_email(self, to_email, detection_type, image_path=None):
        try:
            # Create the email message
            msg = MIMEMultipart()
            msg["From"] = self.EMAIL_APP_ACCOUNT
            msg["To"] = to_email
            msg["Subject"] = f"This is the detection of {detection_type} from the app" 

            # Attach the email body
            msg.attach(MIMEText("Please take a look!", "plain"))

            # Attach the image if provided
            if image_path:
                try:
                    with open(image_path, "rb") as img_file:
                        img_data = img_file.read()
                        image = MIMEImage(img_data)
                        image.add_header("Content-Disposition", f"attachment; filename={os.path.basename(image_path)}")
                        msg.attach(image)
                except Exception as e:
                    print(f"Failed to attach image: {e}")

            # Connect to the SMTP server
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(self.EMAIL_APP_ACCOUNT, self.EMAIL_APP_PASSWORD)
                # Send the email
                server.sendmail(self.EMAIL_APP_ACCOUNT, to_email, msg.as_string())

            print("Email sent successfully.")
        except Exception as e:
            print(f"Failed to send email: {e}")

    def send_email(self, to_email, subject, body, image_path=None):
        try:
            # Create the email message
            msg = MIMEMultipart()
            msg["From"] = self.EMAIL_APP_ACCOUNT
            msg["To"] = to_email
            msg["Subject"] = subject

            # Attach the email body
            msg.attach(MIMEText(body, "plain"))

            # Attach the image if provided
            if image_path:
                try:
                    with open(image_path, "rb") as img_file:
                        img_data = img_file.read()
                        image = MIMEImage(img_data)
                        image.add_header("Content-Disposition", f"attachment; filename={os.path.basename(image_path)}")
                        msg.attach(image)
                except Exception as e:
                    print(f"Failed to attach image: {e}")

            # Connect to the SMTP server
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(self.EMAIL_APP_ACCOUNT, self.EMAIL_APP_PASSWORD)
                # Send the email
                server.sendmail(self.EMAIL_APP_ACCOUNT, to_email, msg.as_string())

            print("Email sent successfully.")
        except Exception as e:
            print(f"Failed to send email: {e}")