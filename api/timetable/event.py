import re
from datetime import timedelta


class Event:
    def __init__(self, cell, start_time):
        self.start_time = None
        self.end_time = None
        self.course_type = None
        self.group = None
        self.course_name = None
        self.teachers = None

        contents = [child.contents for child in cell.td.children]
        info_string = contents[0][0] if contents[0] else None
        if info_string:
            self.parse_info_string(info_string)
        else:
            duration = cell.rowspan * 5
            self.start_time = str(timedelta(minutes=start_time))[:-3]
            self.end_time = str(timedelta(minutes=start_time + duration))[:-3]
        body_string = contents[1][0] if contents[1] else None
        if body_string:
            self.parse_body_string(body_string)

    def parse_info_string(self, info_string):
        pattern = "(\d{1,2}:\d{2})-(\d{1,2}:\d{2}), (\w*) (.*)"
        match = re.match(pattern, info_string)
        if match:
            self.start_time = match.group(1)
            self.end_time = match.group(2)
            self.course_type = match.group(3)
            self.group = match.group(4)

    def parse_body_string(self, body_string):
        pattern = "(.*) - (.*)"
        match = re.match(pattern, body_string)
        if match:
            self.course_name = match.group(1)
            self.teachers = match.group(2)
        else:
            self.course_name = body_string
