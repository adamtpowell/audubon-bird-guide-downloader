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

def subcommand_get_info(args):
    if args.region != None:
        region_tid = region_id_to_tid(args.region)
    else:
        region_tid = -1

    reset_output()

    bird_ids = get_bird_ids(0, region_tid)

    print("Loading bird info")
    Pool(processes = 8).map(get_bird, bird_ids)

def get_bird(bird_id: str):
    bird_info = get_bird_info(bird_id)
    save_bird_info(bird_info)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog = "bird-guide-downloader"
    )

    subparsers = parser.add_subparsers(required=True)

    get_info_parser = subparsers.add_parser("get-info", description="Download info about each bird.")
    get_info_parser.add_argument('-r', '--region',
        choices = region_to_tid_dict.keys(),
    )
    get_info_parser.set_defaults(func=subcommand_get_info)

    # Parse arguments and run the subcommand
    args = parser.parse_args()
    args.func(args)
