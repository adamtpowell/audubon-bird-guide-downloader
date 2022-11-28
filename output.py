# Saves the files related to a single bird
import json
import requests
import os

def save_bird_media(bird_info: dict):
    bird_id = bird_info["id"]

    illustration = bird_info["illustration"]
    illustration_path = 'output/media/' + illustration["local_url"]

    # Only save the media if it doesn't exist.
    if not os.path.exists(illustration_path):
        with open(illustration_path, 'wb') as f:
            f.write(requests.get(illustration["global_url"]).content)
    else:
        print(f"Illustration already saved for {bird_id}")

    for photograph in bird_info["photographs"]:
        photograph_path = 'output/media/' + photograph["local_url"]

        if not os.path.exists(photograph_path):
            with open(photograph_path, 'wb') as f:
                f.write(requests.get(photograph["global_url"]).content)
        else:
            print(f"Photo already saved for {bird_id}")

    for call in bird_info["calls"]:
        call_path = 'output/media/' + call["local_url"]
        if not os.path.exists(call_path):
            with open(call_path, 'wb') as f:
                f.write(requests.get(call["global_url"]).content)
        else:
            print(f"Call already saved for {bird_id}")

    print(f"Saved media for {bird_info['id']}")

def save_bird_info(bird_info: dict):
    with open(f"output/{bird_info['id']}.bird", "w") as f:
        f.write(json.dumps(bird_info))

    print(f"saved info for {bird_info['id']}")
