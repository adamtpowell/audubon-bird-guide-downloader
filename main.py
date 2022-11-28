from multiprocessing import Pool
import argparse
from output import save_bird_info
from utils import get_bird_info

from utils import region_to_tid_dict, region_id_to_tid, reset_output, get_bird_ids

"""
TODO:

Move downloading info as a subcommand.
Add option for overwriting output
    Otherwise, don't fetch for bird-info files that already exist.
Add option / subcommand for loading media from existing bird-infos.
Add subcommand for outputting an anki deck with given parameters.

Organize utils
"""

def get_bird(bird_id: str):
    bird_info = get_bird_info(bird_id)
    save_bird_info(bird_info)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog = "bird-guide-downloader"
    )
    parser.add_argument('-r', '--region',
        choices = region_to_tid_dict.keys(),
    )

    args = parser.parse_args()

    if args.region != None:
        region_tid = region_id_to_tid(args.region)
    else:
        region_tid = -1

    reset_output()

    bird_ids = get_bird_ids(0, region_tid)

    print("Loading bird info")
    Pool(processes = 8).map(get_bird, bird_ids)
