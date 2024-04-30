"""
The main purpose of this app is to 
notify students of their lecture times 
based on their pdf timetable


It's base features include:
1. Notify student when it is time for a lecture
    including the information about that course 
    such as venue and time-range

Future features include:
1. Identify the time remaining between the current lecture
     and the next
"""


from course import Timetable as tt, Course as crs
import time
from datetime import datetime

# when it is time for the lecture,
# notify me saying
# "how far, it is time for your MTH101 lecture"


def notify(title, message):
    from plyer import notification
    notification.notify(
        message=message,
        title=title,
        app_name='Notyfire',
        timeout=10  # timeout in seconds
    )


c0 = crs('CSC205', 'Monday', '08:00', '09:00', 'Alfa Hall')
c1 = crs('MTH205', 'Monday', '15:00', '16:00', 'Alfa Hall')
c2 = crs('mth201', 'Monday', '17:00', '18:00', 'Alfa Hall')

t = tt()
t.add(c0, c1, c2)

lectures = [c for c in t.courses]

# list of courses i have already notified you of
already_notified = set()
while True:
    current_time = datetime.now().strftime('%H:%M')
    current_time = '08:00'  # proxy
    current_hour = int(current_time.split(":")[0])
    current_minute = int(current_time.split(":")[1])

    for course in lectures:
        if (current_time == course.starttime) and (course not in already_notified):
            notify(f'{course}', f'You have {course} now')
            already_notified.add(course)

        elif course not in already_notified:
            # subtract the course time from the current time to get the time remaining
            time_remaining = (datetime(year=2024, month=4, day=27,
                                       hour=course._start_hour,
                                       minute=course._start_minute) -
                              datetime(year=2024, month=4, day=27,
                                       hour=current_hour,
                                       minute=current_minute))

            print(f'waiting for {course} at {course.starttime}')

    time.sleep(1)
