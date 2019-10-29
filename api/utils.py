import cgi
import sys
from typing import List, Optional, Union

HEADERS = [
    'Status: 200 OK',
    'Content-Type: application/json; charset=utf8',
    'Access-Control-Allow-Origin: *'
]


def print_headers() -> None:
    for header in HEADERS:
        cgi_print(header)
    cgi_print()
    sys.stdout.flush()


def cgi_print(string='') -> None:
    byte_string = f'{string}\n'.encode()
    sys.stdout.buffer.write(byte_string)


def get_url_params(*keys: str) -> Union[Optional[str], List[Optional[str]]]:
    params = cgi.FieldStorage()
    if len(keys) == 1:
        [key] = keys
        return params.getvalue(key)
    else:
        return [params.getvalue(key) for key in keys]
