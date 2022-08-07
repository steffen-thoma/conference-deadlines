import datetime
import difflib
from pathlib import Path
from typing import List

import dateutil.parser

from python.config import project_root
from python.io import save_yaml

from python.models import (
    ConferenceMasterData,
    ConferenceCandidateCFP,
    ConferenceRanking,
    ConferenceDeadline,
)


def clean_wikicfp_title(title: str) -> str:
    wikicfp_replace_strings = ["dagm", "ieee", "--ei", "-", "scopus", "&", "acm"]
    for replace_string in wikicfp_replace_strings:
        title = title.replace(replace_string, "")
    return title


def compute_conference_match_score(
    conference: ConferenceMasterData,
    conference_candidate: ConferenceCandidateCFP,
    cutoff=0.8,
):
    score = len(
        difflib.get_close_matches(
            clean_wikicfp_title(conference_candidate.full_name.lower()),
            [conference.title.lower(), conference.full_name.lower()],
            cutoff=cutoff,
        )
    )
    return score


def compute_conference_ranking_match_score(
    conference: ConferenceDeadline, conference_candidate: ConferenceRanking, cutoff=0.8,
):
    score = len(
        difflib.get_close_matches(
            conference_candidate.title.lower(),
            [conference.title.lower(), conference.full_name.lower()],
            cutoff=cutoff,
        )
    )
    return score


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


def save_updated_data(conference_deadlines: List[ConferenceDeadline], path: Path):
    conference_deadlines = sorted(
        conference_deadlines,
        key=lambda x: get_datetime(x.deadline) \
            if x.deadline.lower() != 'tba' else datetime.datetime(3000, 1, 1)
    )
    save_yaml(path, [c.as_dict() for c in conference_deadlines])


def get_date_format_from_start_and_end(start: datetime.datetime, end: datetime.datetime):
    date = f"{datetime_to_string(start, '%B %d')} - {datetime_to_string(end, '%d, %Y')}" if start.month == end.month \
        else f"{datetime_to_string(start, '%B %d')} - {datetime_to_string(end, '%B %d, %Y')}"
    return date