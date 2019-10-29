#!/home/students/inf/t/tm385898/miniconda3/envs/labmap/bin/python

import cgi
import sys
sys.path.append("../..")

from api.utils import print_headers, cgi_print, get_url_params
from api.timetable.timetable import get_timetable


sys.stderr = sys.stdout


if __name__ == '__main__':
    print_headers()
    room, weekday = get_url_params('room', 'weekday')
    result = get_timetable(room, weekday)
    cgi_print(result)
    sys.stdout.flush()
