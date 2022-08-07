from pathlib import Path

from python.config import csv_path_master_data, csv_path_conferences
from python.io import load_csv, save_csv

project_root = Path(__file__).parent.parent.parent


def update_master_data_from_conferences():
    data = load_csv(csv_path_conferences)
    master_data = load_csv(csv_path_master_data)

    titles = set([r['title'] for r in data])
    for title in titles:
        confs = [r for r in data if r['title'] == title]  # find matching title
        conf = sorted(confs, key=lambda x: int(x['year']), reverse=True)[0]  # use newest conf entry for update
        if conf['title'].lower() not in list(set([c['title'].lower() for c in master_data])):
            master_data.append({
                'title': conf['title'].lower(),
                'full_name': conf['full_name'],
                'wikicpf_query': conf['title'],
                'wikicpf_link': "",
                'ranking': conf['ranking'],
                'hindex': conf['hindex'],
                'sub': conf['sub'],
            })
    save_csv(csv_path_master_data, master_data)


if __name__ == '__main__':
    update_master_data_from_conferences()
