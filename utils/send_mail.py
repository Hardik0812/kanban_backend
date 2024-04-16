import os
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.shortcuts import HttpResponse
from django.template.loader import render_to_string


from dotenv import load_dotenv

from utils.helpers import generate_token

load_dotenv()


def send_verification_email(subject, template, data):
    try:
        context = {"email": data["email"]}
        app_url = os.getenv("APP_URL")

        if template == "verify-register-link.html":
            token = generate_token(data["email"], 2880)
            if token:
                context["path"] = app_url + "/verify-email/"
                context["token"] = token
                context["name"] = data["name"]

        html_body = render_to_string(template, context)

        to_email = data["email"]
        msg = MIMEMultipart()
        msg["From"] = "Kanban <" + os.getenv("ADMIN_EMAIL") + ">"
        msg["To"] = to_email
        msg["Subject"] = subject
        part2 = MIMEText(html_body, "html")
        msg.attach(part2)

        mail_server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        mail_server.ehlo()

        mail_server.login(os.getenv("ADMIN_EMAIL"), os.getenv("EMAIL_PASSWORD"))

        mail_server.sendmail(os.getenv("ADMIN_EMAIL"), msg["To"], msg.as_string())
        mail_server.quit()
        return HttpResponse("Mail Send", status=200)
    except Exception as e:
        print(f"Error sending verification email: {e}")
        return HttpResponse("Failed to send email", status=500)


def send_forgot_password_email(subject, template, data):
    try:
        context = {"email": data["email"]}
        app_url = os.getenv("APP_URL")

        if template == "forgot-password-link.html":
            token = generate_token(data["email"], 2880)
            if token:
                context["reset_link"] = app_url + "reset-password" + "?token="+ token
                print("link", context["reset_link"])
                context["name"] = data["name"]

        html_body = render_to_string(template, context)

        to_email = data["email"]
        msg = MIMEMultipart()
        msg["From"] = "Kanban <" + os.getenv("ADMIN_EMAIL") + ">"
        msg["To"] = to_email
        msg["Subject"] = subject
        part2 = MIMEText(html_body, "html")
        msg.attach(part2)

        mail_server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        mail_server.ehlo()

        mail_server.login(os.getenv("ADMIN_EMAIL"), os.getenv("EMAIL_PASSWORD"))

        mail_server.sendmail(os.getenv("ADMIN_EMAIL"), msg["To"], msg.as_string())
        mail_server.quit()
        return HttpResponse("Mail Send", status=200)
    except Exception as e:
        print(f"Error sending verification email: {e}")
        return HttpResponse("Failed to send email", status=500)


def send_otp_email(subject, template, data):
    try:
        context = {"email": data["email"],
                   "otp":data["otp"]}

        if template == "send-otp.html":
            context["email"] = data["email"]
            context["otp"] = data["otp"]

        html_body = render_to_string(template, context)

        to_email = data["email"]
        msg = MIMEMultipart()
        msg["From"] = "Kanban <" + os.getenv("ADMIN_EMAIL") + ">"
        msg["To"] = to_email
        msg["Subject"] = subject
        part2 = MIMEText(html_body, "html")
        msg.attach(part2)

        mail_server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        mail_server.ehlo()

        mail_server.login(os.getenv("ADMIN_EMAIL"), os.getenv("EMAIL_PASSWORD"))

        mail_server.sendmail(os.getenv("ADMIN_EMAIL"), msg["To"], msg.as_string())
        mail_server.quit()
        return HttpResponse("Mail Send", status=200)
    except Exception as e:
        print(f"Error sending verification email: {e}")
        return HttpResponse("Failed to send email", status=500)