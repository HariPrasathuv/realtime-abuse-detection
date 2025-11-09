import smtplib
from email.message import EmailMessage
import time


def alert_email(text,detectList, to="gammutamilan06@gmail.com"):
    
    SMTP_HOST = "smtp.gmail.com"
    SMTP_PORT = 587
    USER = "hariprasathuv06@gmail.com"
    PASSWORD = "ogrk pdcd kbwn ugyo"
    msg = EmailMessage()

    msg["Subject"] = f"Abuse alert"
    msg["From"] = USER
    msg["To"] = to
    ts = time.strftime("%Y-%m-%d %H:%M:%S")
    #body = f"Time: {ts}\nScore: {abuse_score:.2f}\nTranscript: {transcript}\nAudio: {audio_path}"
    body = f"Time: {ts}\nTranscript: {text}\n"
    for l in detectList:
        body += f"{l[0]} : {l[1]:.2f}\n"
    msg.set_content(body)
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as s:
        s.starttls()
        s.login(USER, PASSWORD)
        s.send_message(msg)
