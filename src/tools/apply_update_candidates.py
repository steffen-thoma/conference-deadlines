from src.config import yaml_path_conferences, yaml_path_conference_updated_candidates
from src.io import load_yaml, save_yaml
from src.scraping.models import ConferenceDeadline


def main():
    conference_deadlines = [
        ConferenceDeadline(**data) for data in load_yaml(yaml_path_conferences)
    ]
    conference_deadlines = {conf.id: conf for conf in conference_deadlines}
    conference_deadline_update_candidates = [
        ConferenceDeadline(**data)
        for data in load_yaml(yaml_path_conference_updated_candidates)
    ]
    conference_deadline_update_candidates = {
        conf.id: conf for conf in conference_deadline_update_candidates
    }
    for id, conf in conference_deadline_update_candidates.items():
        matched_conf = conference_deadlines[id]
        for key, val in conf.as_dict().items():
            if key not in matched_conf.as_dict().keys():
                setattr(matched_conf, key, getattr(conf, key))

    save_yaml(
        yaml_path_conferences, [v.as_dict() for _, v in conference_deadlines.items()],
    )


if __name__ == "__main__":
    main()
