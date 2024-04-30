"""NOTE: 
It is impossible to represent an course in timetable.slots if that course has a time not 
specified in the timetable.timezones list

so seek to solve this problem
"""
from datetime import datetime
class Course:
    def __init__(self, code='', day='', starttime='', endtime='', venue='', **info) -> None:
        time_pattern = r"(?P<hour>[0-2][0-9]):(?P<minute>[0-5][0-9])"
        self.code = code.upper()
        self.day = day
        self.date=datetime.now().date()
        
        self.starttime = starttime
        self._start_hour = int(self.starttime.split(":")[0])
        self._start_minute = int(self.starttime.split(":")[1])
        self.endtime = endtime

        self.time = f'{self.starttime}-{self.endtime}'
        self.venue = venue
        self.type_ = info['type_'] if info.__contains__(
            'type_') else 'L'  # L => lecture by default
    
    def __str__(self) -> str:
        return self.code
    


class Timetable:
    def __init__(self) -> None:

        self.slots = [  # matrix format which only takes strings
            ['', '', '', '', '', '', '', '', '', ''],  # Monday
            ['', '', '', '', '', '', '', '', '', ''],  # Tuesday
            ['', '', '', '', '', '', '', '', '', ''],  # Wednesday
            ['', '', '', '', '', '', '', '', '', ''],  # Thursday
            ['', '', '', '', '', '', '', '', '', ''],  # Friday
            ['', '', '', '', '', '', '', '', '', ''],  # Saturday
        ]

        self.courses = []  # list of courses sorted by day and time

        self.timezones = [
            "08:00-09:00",
            "09:00-10:00",
            "10:00-11:00",
            "11:00-12:00",
            "12:00-12:00",  # for the sake of prayers
            "13:00-14:00",  # for the sake of prayers
            "14:00-15:00",
            "15:00-16:00",
            "16:00-17:00",
            "17:00-18:00"
        ]

        self.days = [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday"
        ]


    def read_pdf(self, path):
        import pdfplumber as plum
        pdf = plum.open(path)
        timetable = pdf.pages[0].extract_tables()[0]

        # clean the matrix1
        timetable.pop(0)

        for each_row in timetable:
            if len(each_row) < 10:
                # force it to be =ten
                each_row.append('')
            else:
                pass

        self.slots=timetable
        self._to_course_obj()

    def _to_course_obj(self):
        """For this method to work properly, you must run the read_pdf() method.
        or fill the slots manually with the appropriate format

        {MTH101(L)\nDINING HALL} ===> {CourseCode(type)\nVenue}
        
        """
        for day, row in zip(self.days, self.slots):
            for time, course in zip(self.timezones, row):
                if course.strip():
                    starttime=time.split('-')[0]
                    endtime=time.split('-')[1]

                    venue=course.split('\n')[-1]
                    type_=course.split('(')[-1].split(')')[0]
                    code=course.split('\n')[0].strip(f'({type_})')

                    c = Course(code, day, starttime,endtime,venue=venue, type_=type_)
                    self.courses.append(c)
        

    def search_by_time(self,time):
        search_result=[]
        for course in self.courses:
            if course.starttime==time:
                search_result.append(course)
        return search_result
    
    def search_by_day(self, day):
        search_result=[]
        for course in self.courses:
            if course.day==day:
                search_result.append(course)
        return search_result
    
    def search_by_venue(self, venue):
        search_result=[]
        for course in self.courses:
            if course.venue==venue:
                search_result.append(course)
        return search_result

    def add(self, *course_objs):
        """Add a course to the timetable
        get the time and date from the course object
        and then place the course there.
        """
        for course in course_objs:
            c = course
        
            loc_y = self.days.index(c.day)
            loc_x = self.timezones.index(c.time)

            # add to the matrix representation
            self.slots[loc_y][loc_x] = f'{c.code}({c.type_})\n{c.venue}'
            

            self.courses.append(course)

    def remove(self, course):
        c = course
        ctime = c.time
        cday = c.day

        loc_y = self.days.index(cday)
        loc_x = self.timezones.index(ctime)
        # remove
        self.slots[loc_y][loc_x] = ''
        return c
    def get_courses(self):
        return self.courses
    
    def __str__(self) -> str:
        return f'{self.slots}'


if __name__ == '__main__':
    c1=Course('MTH102','Monday', '08:00', '09:00','Alfa Hall')
    c2=Course('MTH101','Monday', '08:00', '09:00','Alfa Hall')
    c3=Course('MTH201','Tuesday', '08:00', '09:00','Alfa Hall')
    t = Timetable()
    t.add(c1,c2,c3)
    print(t)