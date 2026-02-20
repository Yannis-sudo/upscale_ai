import pathlib
import json

def get_paths_json():
    current_file = pathlib.Path(__file__).resolve()
    json_file = current_file.parent.parent / "data" / "json" / "path.json"
    with open(json_file, "r") as json_f:
        data = json.load(json_f)
    return data