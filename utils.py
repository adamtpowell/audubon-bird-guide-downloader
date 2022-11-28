import json
from bs4 import BeautifulSoup
import requests
from typing import List
import os
import shutil

def get_bird_ids(starting_page: int, region_tid: int) -> List[str]:
    page_content = curl_bird_list_page(starting_page, region_tid)
    bird_ids: List[str] = []

    soup = BeautifulSoup(page_content, 'html.parser')
    bird_paths = soup.select(".bird-card-grid-container .common-name > a")
    bird_ids = [bird_path['href'].replace("/field-guide/bird/","").replace("https://www.audubon.org", "") for bird_path in bird_paths]

    print("Loading page", starting_page)

    if len(bird_ids) == 0:
        return []
    else:
        return bird_ids + get_bird_ids(starting_page + 1, region_tid)

def reset_output():
    if os.path.isdir("output"):
        shutil.rmtree('output')
    os.makedirs("output")
    os.makedirs("output/media")

# Saves the files related to a single bird
def save_bird(bird_id: str):
    page_content = curl_bird_info_page(bird_id)
    soup = BeautifulSoup(page_content, 'html.parser')

    common_name = soup.find(class_="common-name").string.strip()
    scientific_name = soup.find(class_="scientific-name").string.strip()

    # Illustration
    try:
        illustration_url = soup.select(".illustration > img")[0]['src']
        illustration_url = illustration_url.replace("bird_illustration", "nas_bird_teaser_illustration") # The teaser is larger, for some reason
        illustration_local_path = "audubon-illustration-{}.jpg".format(bird_id)
        with open('output/media/' + illustration_local_path, 'wb') as f:
            f.write(requests.get(illustration_url).content)
    except:
        print("{} failed to find illustration".format(bird_id))

    # Download photographs.
    photograph_elements = soup.select(".grid-gallery__lightbox")
    photograph_local_paths = []
    for i in range(len(photograph_elements)):
        try:
            photograph_url = photograph_elements[i]['data-href']
            photograph_local_paths.append("audubon-photo-{}-{}.jpg".format(bird_id, i))
            with open('output/media/' + photograph_local_paths[i], 'wb') as f:
                f.write(requests.get(photograph_url).content)
        except:
            pass

    # Download calls
    call_parent = soup.find(class_="field-name-field-bird-audio")
    call_elements = call_parent.find_all(class_="bird-audio-item") if call_parent else []

    if len(call_elements) == 0:
        print("No calls for {}".format(bird_id))

    call_local_paths = []
    for index, call_element in enumerate(call_elements):
        button = call_element.find("button")
        audio = call_element.find("audio")

        call_url = audio['src']
        try:
            call_description = button['title'].strip()
        except:
            call_description = "No description found"

        call_local_path = "audubon-sound-{}-{}.mp3".format(bird_id, index)
        call_local_paths.append(call_local_path)
        with open('output/media/' + call_local_path, 'wb') as f:
            f.write(requests.get(call_url).content)

    bird_info = {
        "common_name": common_name,
        "scientific_name": scientific_name,
        "photograph_paths": photograph_local_paths,
        "call_paths": call_local_paths,
    }

    with open(f"output/{bird_id}", "w") as f:
        f.write(json.dumps(bird_info))

    print("{} done.".format(bird_id))


def curl_bird_info_page(bird_id: str) -> str:
    response = requests.get("https://www.audubon.org/field-guide/bird/{}".format(bird_id))
    return response.text

def curl_bird_list_page(page: int, region_tid: int) -> str:
    if region_tid == -1: # -1 means all regions.
        url = "https://www.audubon.org/bird-guide?page={}".format(page)
    else:
        url = "https://www.audubon.org/bird-guide?page={}&field_bird_family_tid=All&field_bird_region_tid={}".format(page, region_tid)

    response = requests.get(url)
    return response.text

region_to_tid_dict = {
    "alaska and the north": 130,
    "california": 116,
    "eastern-canada": 59,
    "florida": 44,
    "great-lakes": 49,
    "mid-atlantic": 83,
    "new-england": 48,
    "northwest": 113,
    "plains": 121,
    "rocky-mountains": 110,
    "southeast": 67,
    "southwest": 119,
    "texas": 66,
    "western-canada": 138
}

def region_id_to_tid(region_name: str) -> int:
    return region_to_tid_dict[region_name]
