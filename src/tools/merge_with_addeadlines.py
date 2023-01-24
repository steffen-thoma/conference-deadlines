import dateutil.parser

from src.config import csv_path_master_data, yaml_path_conferences
from src.io import load_ai_deadlines_data, load_csv, load_yaml, save_yaml
from src.scraping.utils import get_date_format_from_start_and_end

time_format = "%Y-%m-%d %H:%M"


def update_data_with_ai_deadlines_data():
    ad_deadlines = load_ai_deadlines_data(site="ad")
    deadlines_info = load_yaml(yaml_path_conferences, key="id")
    for _, conf_data in ad_deadlines.items():
        conf_data["sub"] = conf_data["sub"].replace("V2X", "AD").replace("IV", "AD").replace("AS", "AD")
        conf_data["title"] = conf_data["title"].replace("/", "-")
        conf_data["id"] = conf_data["title"].lower() + str(conf_data["year"])[2:]
        conf_id = conf_data["id"]
        if ("(ws)" in conf_data.get("title", "").lower() or "(deadline estimated)" in conf_data.get("title", "").lower()):
            continue
        if conf_id.lower() not in list(
            set([c["id"].lower() for c in deadlines_info.values()])
        ):  # conf does not exist
            if conf_data.get("long", None) is not None:
                conf_data["full_name"] = conf_data["long"]
                del conf_data["long"]
            deadlines_info[conf_id] = conf_data
        else:  # conf exists -> overwrite data if mismatch
            conf_match = deadlines_info.get(conf_id)
            for key, val in conf_data.items():
                match_key = (
                    key if key != "long" else "full_name"
                )  # necessary due to renaming of key
                if conf_data[key] != conf_match.get(
                    match_key, None
                ):  # use ai-deadlines data if mismatch
                    conf_match[match_key] = val

    # Adjust data
    for conf_id, conf_data in deadlines_info.items():
        delete_keys = ["host"]
        for key, val in conf_data.items():
            if val == "--":
                delete_keys.append(key)
            if key == "note" and val is not None:
                conf_data[key] = val.replace("<b>NOTE</b>: ", "")
            if key == "date":
                if (
                    conf_data.get("start", None) is not None
                    and conf_data.get("end", None) is not None
                ):
                    start = conf_data["start"]
                    end = conf_data["end"]
                    if isinstance(start, str):
                        start = dateutil.parser.parse(start)
                    if isinstance(end, str):
                        end = dateutil.parser.parse(end)
                    conf_data[key] = get_date_format_from_start_and_end(start, end)
            if "deadline" in key:
                if conf_data["deadline"].lower() == "tba":
                    continue
                date = dateutil.parser.parse(val)
                conf_data[key] = date.strftime(time_format)
        for key in delete_keys:
            conf_data.pop(key, None)
    save_yaml(yaml_path_conferences, list(deadlines_info.values()))


if __name__ == "__main__":
    update_data_with_ai_deadlines_data()
