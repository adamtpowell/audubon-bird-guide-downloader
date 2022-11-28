from multiprocessing import Pool
import argparse

from utils import region_to_tid_dict, region_id_to_tid, reset_output, get_bird_ids, save_bird

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

    print("Loading birds...")
    bird_list = Pool(processes = 8).map(save_bird, bird_ids)

    with open("output/birds.txt", "w") as f:
        f.write("\n".join(bird_list))
