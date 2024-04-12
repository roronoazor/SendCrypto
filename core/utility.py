from django.core.mail import send_mail

def notify_mail(subject="", to=[], html_message=""):
    sending_from = "olufunkefaderera06@gmail.com"
    return send_mail(subject, "", sending_from, to, html_message=html_message)
