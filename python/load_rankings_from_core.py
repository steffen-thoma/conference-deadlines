import csv
import datetime
import os
import time
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import List

import tqdm
from bs4 import BeautifulSoup

table_head = ['Title', 'Acronym', 'Source', 'Rank', 'DBLP', 'hasData?', 'Primary FoR', 'Comments', 'Average Rating']


def get_core_rating_query_results(conference):
    query = "icml"
    year = 2021
    # Update Data
    url = f"http://portal.core.edu.au/conf-ranks/?search={query}&by=all&source=CORE{year}&sort=atitle&page=1"

    try:
        page = urllib.request.urlopen(url)
    except Exception as e:
        print(f"Error: could not open {url}: {e}")
        return []
    soup = BeautifulSoup(page, 'html.parser')
    table = soup.select("div#search table")[0]
    tables_rows = table.find_all('tr')
    del tables_rows[0]  # remove headline
    rankings = []
    for row in tables_rows:
        row_data = row.find_all(['th', 'td'])
        rankings.append({table_head[i]: row_data[i].text.replace("\n", "").strip() for i in range(len(table_head))})
        print("")
    print(rankings)


if __name__ == '__main__':
    get_core_rating_query_results(None)
