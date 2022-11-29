from bs4 import BeautifulSoup
import requests
from typing import List
import os
import shutil
import config

def get_bird_ids(starting_page: int, region_tid: int) -> List[str]:

    page_content = curl_bird_list_page(starting_page, region_tid)
    bird_ids: List[str] = []

    soup = BeautifulSoup(page_content, 'html.parser')
    bird_paths = soup.select(".bird-card-grid-container .common-name > a")
    bird_ids = [bird_path['href'].replace("/field-guide/bird/","").replace("https://www.audubon.org", "") for bird_path in bird_paths]

    print(f"Loading page {starting_page} for region {region_tid_to_id(region_tid)}")

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
def get_bird_info(bird_id: str) -> dict:
    page_content = curl_bird_info_page(bird_id)
    soup = BeautifulSoup(page_content, 'html.parser')

    common_name = soup.find(class_="common-name").string.strip()
    scientific_name = soup.find(class_="scientific-name").string.strip()

    # Illustration
    try:
        illustration_url = soup.select(".illustration > img")[0]['src']
        illustration_url = illustration_url.replace("bird_illustration", "nas_bird_teaser_illustration") # The teaser is larger, for some reason
        illustration_local_url = "audubon-illustration-{}.jpg".format(bird_id)

        illustration = {
            "global_url": illustration_url,
            "local_url": illustration_local_url,
        }
    except:
        illustration = {}
        print("{} failed to find illustration".format(bird_id))

    # Download photographs.
    photographs = []

    photograph_elements = soup.select(".grid-gallery__lightbox")
    for i in range(len(photograph_elements)):
            photograph_global_url = photograph_elements[i]['data-href']
            photograph_local_url = "audubon-photo-{}-{}.jpg".format(bird_id, i)

            photographs.append({
                "global_url": photograph_global_url,
                "local_url": photograph_local_url,
            })

    # Download calls
    calls = []

    call_elements = soup.select(".bird-audio-item")
    for index, call_element in enumerate(call_elements):
        audio = call_element.find("audio")

        call_global_url = audio['src']
        call_local_url = "audubon-sound-{}-{}.mp3".format(bird_id, index)

        calls.append({
            "global_url": call_global_url,
            "local_url": call_local_url,
        })

    print(f"Got info for {bird_id}")

    return {
        "id": bird_id,
        "common_name": common_name,
        "scientific_name": scientific_name,
        "illustration": illustration,
        "photographs": photographs,
        "calls": calls,
    }


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


def region_id_to_tid(region_name: str) -> int:
    return config.region_to_tid_dict[region_name]

def region_tid_to_id(region_tid: str) -> int:
    inverse = {v: k for k, v in config.region_to_tid_dict.items()}

    return inverse[region_tid]
