"""
tracks live training courses on O'Reilly, sends email if anything new found
"""

import requests
from bs4 import BeautifulSoup
import smtplib
import json
from email.mime.text import MIMEText
from email.header import Header


URL = 'https://learning.oreilly.com/live-training/'
sender_email = 'you@gmail.com'
receiver_email = 'you+xihuanni@gmail.com'
blacklist = {'agile', 'leader', 'successful'}

r = requests.get(URL)
soup = BeautifulSoup(r.content, 'html.parser')
ip_prefix = 'https://learning.oreilly.com'
datetime_courses = (t.get('datetime')[:-9] for t in soup.find_all('time'))
names_courses = (soup.find_all('div', {'class': 'title t-title'}))
all_courses = {item.get_text().strip().lower() + ' ' + t: ip_prefix + item.a.get('href')
               for t, item in zip(datetime_courses, names_courses)}
selected_courses = {course: url for course, url in all_courses.items()
                    if not any((topic in course for topic in blacklist))}


# to create the courses data for the first time
try:
    with open('checked_courses.json', 'x') as f:
        json.dump(selected_courses, f)
except FileExistsError:
    pass

with open('checked_courses.json') as f:
    previous_courses = json.load(f)

new_courses = {name: selected_courses[name]
               for name in selected_courses.keys() ^ previous_courses.keys() & selected_courses.keys()}


def send_email():
    smtp_server = 'smtp.gmail.com'
    port = 587
    with smtplib.SMTP(smtp_server, port) as server:

        server.ehlo()
        server.starttls()
        server.ehlo()

        server.login('you@gmail.com', 'password')

        subject = 'New courses you might be interested in'
        body = '\n'.join((key + ':' + value for key, value in new_courses.items()))

        msg = MIMEText(body)
        msg['Subject'] = Header(subject)

        server.sendmail(
            sender_email,
            receiver_email,
            msg.as_string()
        )
        print('email has been sent.')


if new_courses:
    with open('checked_courses.json', 'w') as f:
        json.dump(selected_courses, f)

    send_email()
