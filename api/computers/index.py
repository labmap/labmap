#!/home/students/inf/t/tm385898/miniconda3/envs/labmap/bin/python

import cgi
import json
import sys
sys.path.append("../..")

from api.utils import print_headers, cgi_print, get_url_params
from src.database import initialize_database, Computer

sys.stderr = sys.stdout


if __name__ == '__main__':
    print_headers()
    room = get_url_params('room')
    session = initialize_database('../../database.db')
    computers = session.query(Computer)
    if room is not None:
        computers = computers.filter_by(room=int(room))
    computers_json = json.dumps([computer.as_dict() for computer in computers])
    cgi_print(computers_json)
    sys.stdout.flush()
