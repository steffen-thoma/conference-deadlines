import datetime

import dateutil.parser

from python.config import yaml_path_conferences, project_root
from python.io import save_yaml, save_csv

datetime_format = '%Y/%m/%d %H:%M'
date_format = '%Y/%m/%d'
format_wikicpf = "%b %d, %Y"
format_conf_date = "%B %d, %Y"
csv_path = project_root / "_data/conferences.csv"


def get_datetime(datetime_string: str):
    date = None
    for format in ["%y/%d/%m %H:%M", "%m/%d/%Y %H:%M", "%m/%d/%Y"]:
        try:
            date = datetime.datetime.strptime(datetime_string.strip(), format)
            break
        except Exception as e:
            # print(f"{e}          [for {format}]")
            pass
    if date is None:
        date = dateutil.parser.parse(datetime_string)
    return date


def datetime_to_string(dt, format):
    return dt.strftime(format).lstrip("0").replace(" 0", " ").replace("/0", "/")


def save_udapted_data(conference_deadlines):
    conference_deadlines = sorted(
        conference_deadlines,
        key=lambda x: get_datetime(x['deadline']) \
            if x['deadline'].lower() != 'tba' else datetime.datetime(3000, 1, 1)
    )
    save_yaml(yaml_path_conferences, conference_deadlines)
    save_csv(csv_path, conference_deadlines)


def get_date_format_from_start_and_end(start: datetime.datetime, end: datetime.datetime):
    date = f"{datetime_to_string(start, '%B %d')} - {datetime_to_string(end, '%d, %Y')}" if start.month == end.month \
        else f"{datetime_to_string(start, '%B %d')} - {datetime_to_string(end, '%B %d, %Y')}"
    return date