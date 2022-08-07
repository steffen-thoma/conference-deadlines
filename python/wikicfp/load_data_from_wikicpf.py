import datetime
import time
import urllib.request
from pathlib import Path
from typing import List, Dict

import tqdm
from bs4 import BeautifulSoup

from python.config import yaml_path_conferences, csv_path_master_data
from python.core.load_rankings_from_core import scrape_core_ratings, get_matching_core_ranking
from python.io import load_yaml, load_csv
from python.models import ConferenceMasterData, ConferenceCandidateCFP, ConferenceDeadline
from python.utils import compute_conference_match_score
from python.wikicfp.utils import date_format, format_conf_date, get_datetime, datetime_to_string, save_udapted_data, \
    get_date_format_from_start_and_end

project_root = Path(__file__).parent.parent


def scrape_conference_candidates_from_wikicpf(conference: ConferenceMasterData) -> List[ConferenceCandidateCFP]:
    # Update Data
    if conference.wikicfp_link is None or conference.wikicfp_link == "":
        url = f"http://wikicfp.com/cfp/servlet/tool.search?q={conference.wikicfp_query}&year=f"
        table_id = 1
    else:
        url = conference.wikicfp_link
        table_id = 3

    try:
        page = urllib.request.urlopen(url)
    except Exception as e:
        print(f"Error: could not open {url}: {e}")
        return []
    soup = BeautifulSoup(page, 'html.parser')
    table = soup.select("div.contsec table")[table_id]
    tables_rows = table.find_all('tr')
    if len(tables_rows) == 0:
        return []
    headline = tables_rows.pop(0)
    content_rows = [[tables_rows[i], tables_rows[i + 1]] for i in range(0, len(tables_rows), 2)]
    conference_candidates = []
    for i, row in enumerate(content_rows):
        row_data = [subrow.find_all(['th', 'td']) for subrow in row]
        row_data = sum(row_data, [])
        try:
            year = int(row_data[0].text.split(" ")[-1])
            # year = get_datetime(row_data[2].text.split("-")[0].strip()).year
            conf_data = {
                'title': row_data[0].text,
                'wikicfp_link': f"http://wikicfp.com{row_data[0].find_all('a')[0]['href']}",
                'full_name': row_data[1].text,
                'year': year,
                # 'date': row_data[2].text,
                # 'location': row_data[3].text,
                # 'deadline': row_data[4].text,
            }
            conference_candidates.append(ConferenceCandidateCFP(**conf_data))
        except Exception as e:
            print(f"Error with {[r.text for r in row_data]}: {e}")
    return conference_candidates


def extract_data_from_website(url) -> Dict:
    def get_data(keyword: str, resources):
        candidates = [r for r in resources if r[0].text.strip().lower() == keyword.lower()]
        if len(candidates) == 1:
            return candidates[0][1].text

    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page, 'html.parser')

    # Extract Conference Info
    table = soup.select("div.contsec table.gglu")[0]
    tables_rows = table.find_all('tr')
    row_data = [row.find_all(['th', 'td']) for row in tables_rows]
    conf_data = {
        'date': get_data('when', row_data),
        'location': get_data('where', row_data),
        'deadline_abstract': get_data('abstract registration due', row_data),
        'deadline_submission': get_data('submission deadline', row_data),
        'notification_date': get_data('notification due', row_data),
        'final_version': get_data('final version due', row_data),
        'wikicfp': url,
    }

    # Extract Conference Link
    link_table = soup.select("div.contsec")[0]
    link_candidates = [f.text for f in link_table.find_all('td') if "Link:" in f.text]
    if len(link_candidates) == 1:
        link = link_candidates[0].replace("Link:", "")
        conf_data['link'] = link

    conf_data = {key: val.replace('\n', '').replace("\t", "").strip() for key, val in conf_data.items() if val}
    return conf_data


def find_conference_from_candidates(conference: ConferenceMasterData, conference_candidates: List[ConferenceCandidateCFP]) -> List[ConferenceCandidateCFP]:
    current_year = datetime.datetime.now().year

    # Only conferences next year
    best_candidates = [c for c in conference_candidates
                       if c.year - current_year in [-1, 0, 1] and compute_conference_match_score(conference, c) > 0.8]
    if len(best_candidates) == 0:
        print(f"WARNING: no candidates found for {conference.title} ({conference.full_name}); \n"
              f"Candidates: {conference_candidates}")
    return best_candidates


def convert_wikicfp2deadline(conference_data, conference: ConferenceMasterData) -> ConferenceDeadline:
    start, end = [get_datetime(d) for d in conference_data['date'].split("-")]
    abstract_deadline = f"{datetime_to_string(get_datetime(conference_data['deadline_abstract']), date_format)} 23:59" \
        if 'deadline_abstract' in conference_data.keys() else ""
    data = {
        "title": conference.title.upper(),
        "full_name": conference_data['full_name'],
        "hindex": conference.hindex,
        "ranking": conference.ranking,
        "year": str(conference_data['year']),
        "id": f"{conference.title}{str(conference_data['year'])[2:]}",
        "link": conference_data['link'] if 'link' in conference_data.keys() else None,
        "deadline": f"{datetime_to_string(get_datetime(conference_data['deadline_submission']), date_format)} 23:59",
        "abstract_deadline": abstract_deadline,
        "timezone": "",
        "start": datetime_to_string(start, date_format),
        "end": datetime_to_string(end, date_format),
        "date": get_date_format_from_start_and_end(start, end),
        "place": conference_data['location'] if 'location' in conference_data.keys() else None,
        "sub": conference.sub,
        "note": f"Abstract deadline: {datetime_to_string(get_datetime(conference_data['deadline_abstract']), format_conf_date)}" if abstract_deadline != "" else "",
        'wikicfp': conference_data['wikicfp'],
    }
    return ConferenceDeadline(**data)



def update_conferences_from_cpf():
    conference_deadlines = [ConferenceDeadline(**data) for data in load_yaml(yaml_path_conferences)]
    conference_masterdatas = [ConferenceMasterData(**conf_dict) for conf_dict in load_csv(csv_path_master_data)][0:1]
    new_conference_deadlines = scrape_new_conference_data(conference_masterdatas)
    print(new_conference_deadlines)
    # todo: save in new file
    # update_conference_deadlines(conference_deadlines, new_conference_deadlines)
    # save_udapted_data(conference_deadlines)
    return new_conference_deadlines


def update_conference_deadlines(conference_deadlines: List[ConferenceDeadline], new_conference_deadlines: List[ConferenceDeadline]):
    for new_conference in new_conference_deadlines:
        if new_conference.id in [c.id for c in conference_deadlines]:  # if already exists
            existing_entry = [c for c in conference_deadlines if c.id == new_conference.id][0]
            for key, val in existing_entry.items():
                if val != new_conference[key]:
                    if new_conference[key] != "":
                        if val in ["", "TBA", None]:
                            existing_entry[key] = new_conference[key]
                            print(f"{new_conference['id']}: added key {key}: {new_conference[key]}")
                        else:
                            print(f"{new_conference['id']}: "
                                  f"key {key} values: {val} / {new_conference[key]} (existing/new)")
        else:
            print(f"{new_conference['id']}: added conference: {new_conference}")
            conference_deadlines.append(new_conference)


def scrape_new_conference_data(conferences: List[ConferenceMasterData]) -> List[ConferenceDeadline]:
    new_conference_deadlines = []
    for conference in tqdm.tqdm(conferences):
        new_conference_deadline = scrape_new_conference_deadline(conference)
        if new_conference_deadline is not None:
            conference_ranking = get_matching_core_ranking(new_conference_deadline)
            if conference_ranking is not None:
                new_conference_deadline.ranking = conference_ranking.rank
                new_conference_deadline.ranking_link = conference_ranking.link
            new_conference_deadlines.append(new_conference_deadline)
    return new_conference_deadlines


def scrape_new_conference_deadline(conference: ConferenceMasterData) -> ConferenceDeadline:
    conference_candidates = scrape_conference_candidates_from_wikicpf(conference)
    best_conference_candidates = find_conference_from_candidates(conference, conference_candidates)
    for conference_data in best_conference_candidates:
        time.sleep(5)  # max 1 request every 5 seconds, see http://wikicfp.com/cfp/data.jsp
        try:
            conference_details = extract_data_from_website(conference_data.wikicfp_link)
            conference_deadline = convert_wikicfp2deadline({**conference_details, **conference_data.__dict__}, conference)
            return conference_deadline
        except Exception as e:
            print(f"Error {conference.title}: {e} (candidate: {conference_data})")
    time.sleep(5)  # max 1 request every 5 seconds, see http://wikicfp.com/cfp/data.jsp


if __name__ == '__main__':
    update_conferences_from_cpf()
