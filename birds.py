from bs4 import BeautifulSoup
import requests
from typing import List
import os
from tqdm import tqdm
import shutil
import sys
from multiprocessing import Pool, Lock

# Returns a list of all of the bird urls.
def get_bird_ids(starting_page: int, region_tid: int) -> List[str]:
    page_content = curl_bird_list_page(starting_page, region_tid)
    bird_ids: List[str] = []

    soup = BeautifulSoup(page_content, 'html.parser')
    bird_paths = soup.select(".bird-card-grid-container .common-name > a")
    bird_ids = [bird_path['href'].replace("/field-guide/bird/","") for bird_path in bird_paths]

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

def save_bird(bird_id: str) -> str:
    page_content = curl_bird_info_page(bird_id)
    soup = BeautifulSoup(page_content, 'html.parser')

    # Holds each tab seperated card field in the following order:
    # Common Name
    # Scientific Name
    # Illustration <img> tag
    # Photo <img> tag
    # for 10 calls:
    #   Call audio link
    #   Call label

    fields: List[str] = []

    common_name = soup.find(class_="common-name").string.strip()
    fields.append(common_name)

    scientific_name = soup.find(class_="scientific-name").string.strip()
    fields.append(scientific_name)

    # Illustration
    try:
        illustration_url = soup.select(".illustration > img")[0]['src']
        illustration_url = illustration_url.replace("bird_illustration", "nas_bird_teaser_illustration") # The teaser is larger, for some reason
        illustration_local_path = "audubon-illustration-{}.jpg".format(bird_id)
        with open('output/media/' + illustration_local_path, 'wb') as f:
            f.write(requests.get(illustration_url).content)
        fields.append('"<img src=""{}"">"'.format(illustration_local_path))
    except:
        print("{} failed to find illustration".format(bird_id))
        fields.append("IMAGE NOT FOUND")

    # Photograph
    try:
        photograph_url = soup.select(".grid-gallery__lightbox")[0]['data-href']
        photograph_local_path = "audubon-photo-{}.jpg".format(bird_id)
        with open('output/media/' + photograph_local_path, 'wb') as f:
            f.write(requests.get(photograph_url).content)
        fields.append('"<img src=""{}"">"'.format(photograph_local_path))
    except:
        print("{} failed to find photo".format(bird_id))
        fields.append("IMAGE NOT FOUND")

    # Calls
    call_parent = soup.find(class_="field-name-field-bird-audio")
    call_elements = call_parent.find_all("a") if call_parent else []

    if len(call_elements) == 0:
        print("No calls for {}".format(bird_id))

    for index, call_element in enumerate(call_elements):

        call_url = call_element['href']
        try:
            call_description = call_element.contents[1].strip()
        except:
            call_description = "No description found"

        call_local_path = "audubon-call-{}-{}.mp3".format(bird_id, index)
        with open('output/media/' + call_local_path, 'wb') as f:
            f.write(requests.get(call_url).content)
        fields.append("[sound:{}]".format(call_local_path))
        fields.append(call_description)

    fields = fields[:24]

    # Blank out the rest of the fields cause anki dumb
    while len(fields) < 24:
        fields.append("")

    return "\t".join(fields)

def curl_bird_info_page(bird_id: str) -> str:
    response = requests.get("https://www.audubon.org/field-guide/bird/{}".format(bird_id))
    return response.text

def curl_bird_list_page(page: int, region_tid: int) -> str:
    response = requests.get("https://www.audubon.org/bird-guide?page={}&field_bird_family_tid=All&field_bird_region_tid={}".format(page, region_tid))
    return response.text

if __name__ == "__main__":
    # TODO: Give a region selector.

    reset_output()
    
    bird_ids = get_bird_ids(0, 48)
    
    print("Loading birds...")
    bird_list = Pool(processes = 16).map(save_bird, bird_ids)

    with open("output/birds.txt", "w") as f:
        f.write("\n".join(bird_list))