import json
import requests
from urllib.parse import urlencode
from parse import parse_html

URLS_JSON = 'timetable.json'

URL_PARAMETERS = {
    "plan_format": "html",
    "plan_showSettings": 1,
    "plan_showStartTime": 1,
    "plan_showEndTime": 1,
    "plan_showTypeShort": 1,
    "plan_showTypeFull": 0,
    "plan_showGroupNumber": 1,
    "plan_showCourseName": 1,
    "plan_showCourseCode": 0,
    "plan_showBuildingCode": 0,
    "plan_showLecturers": 1,
    "plan_overridePrintWidth": 1,
    "plan_colorScheme": "default"
}


def serialize(self):
    return self.__dict__


def get_room_url(room_number):
    with open(URLS_JSON) as file:
        url_dict = json.load(file)
    room_url = url_dict[room_number] + "&" + urlencode(URL_PARAMETERS)
    return room_url


def translate_keys(dictionary):
    translation_dict = {
        "": "",
        "Poniedziałek": "monday",
        "Wtorek": "tuesday",
        "Środa": "wednesday",
        "Czwartek": "thursday",
        "Piątek": "friday",
        "Sobota": "saturday",
        "Niedziela": "sunday"
    }
    return {
        translation_dict[key]: dictionary[key]
        for key in dictionary
    }


def filter_keys(dictionary, weekday):
    return {
        weekday: dictionary[weekday]
    }


def get_timetable(room_number, weekday=None):
    room_url = get_room_url(room_number)
    html = requests.get(room_url).content
    result_dict = parse_html(html)
    result_dict = translate_keys(result_dict)
    if weekday:
        result_dict = filter_keys(result_dict, weekday)
    result_json = json.dumps(result_dict, default=serialize)
    return result_json
