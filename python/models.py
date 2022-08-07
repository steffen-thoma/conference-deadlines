from dataclasses import dataclass


@dataclass
class ConferenceMasterData:
    title: str = ""
    full_name: str = ""
    wikicfp_query: str = ""
    wikicfp_link: str = ""
    ranking: str = ""
    sub: str = ""
    hindex: str = ""


@dataclass
class ConferenceCandidateCFP:
    title: str = ""
    wikicfp_link: str = ""
    full_name: str = ""
    year: int = None


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
