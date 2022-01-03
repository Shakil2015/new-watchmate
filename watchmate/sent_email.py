from django.core import mail
connection = mail.get_connection()

# Manually open the connection
connection.open()