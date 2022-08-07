from typing import Dict
from dataclasses import dataclass


def attributes_as_dict(instance):
    res = {}
    for key, val in instance.__dict__.items():
        if key in ["__len__"]:
            continue
        if val not in ["", None]:
            res[key] = val
    return res


@dataclass
class ConferenceMasterData:
    title: str = ""
    full_name: str = ""
    wikicfp_query: str = ""
    wikicfp_link: str = ""
    ranking: str = ""
    sub: str = ""
    hindex: str = ""

    def as_dict(self) -> Dict:
        return attributes_as_dict(self)


@dataclass
class ConferenceCandidateCFP:
    title: str = ""
    wikicfp_link: str = ""
    full_name: str = ""
    year: int = None

    def as_dict(self) -> Dict:
        return attributes_as_dict(self)


@dataclass
class ConferenceRanking:
    title: str  # full_name in other classes
    acronym: str  # title in other classes
    source: str
    rank: str
    dblp: str
    hasdata: str
    primary_for: str
    comments: str
    average_rating: str
    link: str

    def as_dict(self) -> Dict:
        return attributes_as_dict(self)


@dataclass
class ConferenceDeadline:
    title: str = ""
    year: int = None
    id: str = ""
    full_name: str = ""
    link: str = ""
    deadline: str = ""
    abstract_deadline: str = ""
    timezone: str = ""
    place: str = ""
    date: str = ""
    start: str = ""
    end: str = ""
    paperslink: str = ""
    pwclink: str = ""
    hindex: int = None
    sub: str = ""
    ranking: str = ""
    ranking_link: str = ""
    note: str = ""
    wikicfp: str = ""
    wikicfp_comment: str = ""

    def as_dict(self) -> Dict:
        return attributes_as_dict(self)

    def update_from_candidate(self, new_conference: "ConferenceDeadline"):
        updated = False
        for key, val in self.as_dict().items():
            if val != new_conference.as_dict()[key]:
                if new_conference.as_dict()[key] not in ["", None]:
                    updated = True
                    if isinstance(val, str):
                        self.as_dict()[key] += f"[{new_conference.as_dict()[key]}]"
                    else:
                        self.as_dict()[key] += f"[{new_conference.as_dict()[key]} (type: {type(val)}]"
        return updated
