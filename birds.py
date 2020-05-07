from bs4 import BeautifulSoup
import requests
from typing import List

# Returns a list of all of the bird urls.
def get_bird_ids(starting_page: int, region_tid: int) -> List[str]:
    page_content = curl_bird_list_page(starting_page, region_tid)
    bird_ids: List[str] = []

    soup = BeautifulSoup(page_content, 'html.parser')
    bird_paths = soup.select(".bird-card-grid-container .common-name > a")
    bird_ids = [bird_path['href'].replace("/field-guide/bird/") for bird_path in bird_paths]

    print("Loading page", starting_page)

    if len(bird_ids) == 0:
        return []
    else:
        return bird_ids + get_bird_ids(starting_page + 1, region_tid)

def curl_bird_list_page(page: int, region_tid: int) -> str:
    response = requests.get("https://www.audubon.org/bird-guide?page={}&field_bird_family_tid=All&field_bird_region_tid={}".format(page, region_tid))
    return response.text

# TODO: Give a region selector.

if __name__ == "__main__":
    bird_ids = get_bird_ids(0, 48)