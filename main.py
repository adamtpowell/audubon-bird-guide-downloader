import glob
import itertools
import json
from multiprocessing import Pool
import argparse
import os
from output import save_bird_info, save_bird_media
import utils
from itertools import repeat
import config

from utils import region_id_to_tid, reset_output, get_bird_ids

"""
TODO:
Add subcommand for outputting an anki deck with given parameters.

Organize utils
"""

# This can't be dynamic, since it needs to be pickleable.
def get_bird_info(args): # Don't grab or overwrite existing birds unless the flag is set to true.
    (bird_id, overwrite) = args
    if os.path.exists(f"./output/{bird_id}.bird") and not overwrite:
        print(f"The file for {bird_id} already exists")
        return

    bird_info = utils.get_bird_info(bird_id)
    save_bird_info(bird_info)

def subcommand_get_info(args):
    if args.region != None:

        region_tids = map(region_id_to_tid, args.region)
    else:
        region_tids = [-1]

    bird_ids = itertools.chain(*[
        get_bird_ids(0, region_tid)
        for region_tid in region_tids
    ])

    Pool(processes = 8).map(get_bird_info, zip(bird_ids, repeat(args.overwrite)))

def subcommand_get_media(args):
    # Load bird info from files.
    bird_files = glob.glob("./output/*.bird")

    def bird_info_from_file(path):
        with open(path, "r") as f:
            return json.loads("\n".join(f.readlines()))

    bird_infos = [bird_info_from_file(path) for path in bird_files]

    Pool(processes = 8).map(save_bird_media, bird_infos)

def subcommand_reset_output(args):
    reset_output()

    print("Output reset.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog = "bird-guide-downloader"
    )
    subparsers = parser.add_subparsers(required=True)

    get_info_parser = subparsers.add_parser("get-info", description="Download info about each bird.")
    get_info_parser.add_argument('-r', '--region', nargs="*",
        choices = config.region_to_tid_dict.keys(),
    )
    get_info_parser.add_argument('-o', '--overwrite', action="store_true", default=False)
    get_info_parser.set_defaults(func=subcommand_get_info)

    get_media_parser = subparsers.add_parser("get-media")
    get_media_parser.set_defaults(func=subcommand_get_media)

    reset_output_parser = subparsers.add_parser("reset-output")
    reset_output_parser.set_defaults(func=subcommand_reset_output)

    # Parse arguments and run the subcommand
    args = parser.parse_args()
    args.func(args)
