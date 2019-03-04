from flask_mail import Message
from flask import render_template
from . import mail

subject_pref = "BLOG"

def mail_message(subject,template,to,**kwargs):
    
    sender_email = "uwitonzeq@gmail.com"
    sender_password = "wito123456"

    email = Message(subject, sender=sender_email, recipients=[to])
    email.body= render_template(template + ".txt",**kwargs)
    email.html = render_template(template + ".html",**kwargs)
    mail.send(email)