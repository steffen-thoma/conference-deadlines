import datetime
import difflib
from pathlib import Path
from typing import List

from python.io import save_yaml

from python.scraping.models import (
    ConferenceMasterData,
    ConferenceCandidateCFP,
    ConferenceRanking,
    ConferenceDeadline,
)
from python.scraping.utils_datetime import get_datetime


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


def save_updated_data(conference_deadlines: List[ConferenceDeadline], path: Path):
    conference_deadlines = sorted(
        conference_deadlines,
        key=lambda x: get_datetime(x.deadline) \
            if x.deadline.lower() != 'tba' else datetime.datetime(3000, 1, 1)
    )
    save_yaml(path, [c.as_dict() for c in conference_deadlines])


