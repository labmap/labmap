#!/home/students/inf/t/tm385898/public_html/labmap/venv/bin/python

import cgi
import sys
import timetable

HEADERS = [
    'Status: 200 OK',
    'Content-Type: application/json; charset=utf8',
    'Access-Control-Allow-Origin: *'
]

sys.stderr = sys.stdout


def cgi_print(string=''):
    byte_string = (string + '\n').encode()
    sys.stdout.buffer.write(byte_string)


def print_headers():
    for header in HEADERS:
        cgi_print(header)
    cgi_print()
    sys.stdout.flush()


if __name__ == '__main__':
    print_headers()
    query_parameters = cgi.FieldStorage()
    room_number = query_parameters.getvalue('room')
    weekday = query_parameters.getvalue('weekday')
    result = timetable.get_timetable(room_number, weekday)
    cgi_print(result)
    sys.stdout.flush()
