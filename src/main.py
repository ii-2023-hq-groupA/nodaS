from scrap_tabelog import Tabelog
import argparse

BASE_URL = "https://tabelog.com/tokyo/rstLst/ramen/"


def main(args):
    print(f"search : {args.ward} ... begin: {args.start} -> end: {args.end}")
    tabelog = Tabelog(
        base_url=BASE_URL, p_ward=args.ward)
    tabelog.do_scrape(
        test_mode=False, begin_page=args.start, end_page=args.end)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--start', type=int, default=1)
    parser.add_argument('-e', '--end', type=int, default=10)
    parser.add_argument('-w', '--ward', type=str, default='文京区')
    args = parser.parse_args()
    main(args)
