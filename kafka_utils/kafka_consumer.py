from kafka import KafkaConsumer
import json
import smtplib
from email.mime.text import MIMEText

def send_email(to_email, subject, body):
    sender = 'yourownemail@gmail.com'  
    password = 'app password'

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = to_email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(sender, password)
            smtp.sendmail(sender, to_email, msg.as_string())
            print(f"Email sent to {to_email}")
    except smtplib.SMTPAuthenticationError as e:
        print("Authentication failed:", e)
    except Exception as e:
        print("Email send failed:", e)

def main():
    consumer = KafkaConsumer(
        'resume_evaluation_results',
        bootstrap_servers='localhost:9092',
        value_deserializer=lambda x: json.loads(x.decode('utf-8')),
        auto_offset_reset='earliest',
        enable_auto_commit=True
    )

    print("Listening to Kafka topic 'resume_evaluation_results'...")

    for message in consumer:
        data = message.value
        email = data.get('email')
        score = data.get('similarity', 0)

        print(f"Received message: {data}")

        if email and score >= 20:
            subject = "Congratulations on your Resume Evaluation"
            body = f"Dear Candidate,\n\nCongratulations! You have scored {score} in the resume evaluation and have been shortlisted.\n\nBest regards,\nHR Team"
            send_email(email, subject, body)
        else:
            print(f"Candidate {email} has score {score}, not sending email.")

if __name__ == "__main__":
    main()
