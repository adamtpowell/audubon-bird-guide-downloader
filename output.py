# Saves the files related to a single bird
import json
import requests

def save_bird_media(bird_info: dict):
    illustration = bird_info["illustration"]
    with open('output/media/' + illustration["local_url"], 'wb') as f:
        f.write(requests.get(illustration["global_url"]).content)

    for photograph in bird_info["photographs"]:
        with open('output/media/' + photograph["local_url"], 'wb') as f:
            f.write(requests.get(photograph["global_url"]).content)

    for call in bird_info["calls"]:
        with open('output/media/' + call["local_url"], 'wb') as f:
            f.write(requests.get(call["global_url"]).content)


    print(f"Saved media for {bird_info['id']}")

def save_bird_info(bird_info: dict):
    with open(f"output/{bird_info['id']}.bird", "w") as f:
        f.write(json.dumps(bird_info))

    print(f"saved info for {bird_info['id']}")
