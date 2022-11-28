from multiprocessing import Pool
import argparse
import os
from output import save_bird_info
from utils import get_bird_info
from itertools import repeat

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

# This can't be dynamic, since it needs to be pickleable.
def get_bird(args): # Don't grab or overwrite existing birds unless the flag is set to true.
    (bird_id, overwrite) = args
    if os.path.exists(f"./output/{bird_id}") and not overwrite:
        print(f"The file for {bird_id} already exists")
        return

    bird_info = get_bird_info(bird_id)
    save_bird_info(bird_info)

def subcommand_get_info(args):
    if args.region != None:
        region_tid = region_id_to_tid(args.region)
    else:
        region_tid = -1

    bird_ids = get_bird_ids(0, region_tid)

    Pool(processes = 8).map(get_bird, zip(bird_ids, repeat(args.overwrite)))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog = "bird-guide-downloader"
    )
    subparsers = parser.add_subparsers(required=True)

    get_info_parser = subparsers.add_parser("get-info", description="Download info about each bird.")
    get_info_parser.add_argument('-r', '--region',
        choices = region_to_tid_dict.keys(),
    )
    get_info_parser.add_argument('-o', '--overwrite', action="store_true")

    get_info_parser.set_defaults(func=subcommand_get_info)

    get_media_parser = subparsers.add_parser("get-media")

    reset_output_parser = subparsers.add_parser("reset-output")

    # Parse arguments and run the subcommand
    args = parser.parse_args()
    args.func(args)
