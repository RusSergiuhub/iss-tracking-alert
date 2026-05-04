import requests
from datetime import datetime
import smtplib
import time
import pandas as pd
import os

MY_LAT = 40.701731
MY_LONG = 20.592041

my_email = "your_email@gmail"
my_pass = "your_password"

def log_progress(message):
    timestamp_format = "%Y-%m-%d %H:%M:%S"
    now = datetime.now()
    timestamp = now.strftime(timestamp_format)

    with open("code_log.txt", "a") as f:
        f.write(timestamp + " : " + message + "\n")

def get_iss_data():
    try:
        response = requests.get(
            url="http://api.open-notify.org/iss-now.json",
            timeout=10
        )
        response.raise_for_status()

        data = response.json()

        iss_lat = float(data["iss_position"]["latitude"])
        iss_long = float(data["iss_position"]["longitude"])

        is_overhead = (
            MY_LAT - 5 <= iss_lat <= MY_LAT + 5 and
            MY_LONG - 5 <= iss_long <= MY_LONG + 5
        )

        log_progress(f"ISS position checked: lat={iss_lat}, long={iss_long}")

        if is_overhead:
            log_progress("The ISS is over our heads!")
        else:
            log_progress("ISS is not over our heads")

        return iss_lat, iss_long, is_overhead

    except requests.exceptions.RequestException as error:
        log_progress(f"API request failed: {error}")
        return None, None, False

def save_data(timestamp, iss_lat, iss_long, is_overhead, email_sent):
    new_data = {
        "timestamp": [timestamp],
        "iss_latitude": [iss_lat],
        "iss_longitude": [iss_long],
        "user_latitude": [MY_LAT],
        "user_longitude": [MY_LONG],
        "is_overhead": [is_overhead],
        "email_sent": [email_sent]
    }

    df = pd.DataFrame(new_data)

    file_exists = os.path.isfile("iss_tracking_data.csv")

    df.to_csv("iss_tracking_data.csv", mode="a", index=False, header=not file_exists)

    log_progress("ISS tracking data saved to CSV")

def send_email_alert():
    try:
        connection = smtplib.SMTP("smtp.gmail.com", 587)
        connection.starttls()
        connection.login(my_email, my_pass)

        connection.sendmail(
            from_addr=my_email,
            to_addrs=my_email,
            msg="Subject: ISS Alert\n\nLook up! The ISS is above your location."
        )

        connection.close()

        log_progress("Alert System Online -> Email sent")
        return True

    except Exception as error:
        log_progress(f"Email sending failed: {error}")
        return False

log_progress("Initiating ISS Tracking System")

while True:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    iss_lat, iss_long, is_overhead = get_iss_data()
    email_sent = False

    if iss_lat is not None and iss_long is not None:
        if is_overhead:
            email_sent = send_email_alert()

        save_data(
            timestamp=timestamp,
            iss_lat=iss_lat,
            iss_long=iss_long,
            is_overhead=is_overhead,
            email_sent=email_sent
        )

    time.sleep(60)