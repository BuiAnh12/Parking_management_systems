from email_sender.sender import Sender

# Example usage
recipient = "buianh120403@gmail.com"
subject = "Test Email with Attachment"
body = "This email contains an attached picture."
image_path = "./video/image.png"

sender = Sender()
sender.send_email(recipient, subject, body, image_path=image_path)
