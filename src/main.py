from scrap_tabelog import Tabelog
import argparse

BASE_URL = "https://tabelog.com/tokyo/R9/rstLst/ramen/"


def main(args):
    print(f"search : begin: {args.start} -> end: {args.end}")
    tabelog = Tabelog(base_url=BASE_URL,
                      begin_page=args.start, end_page=args.end)
    tabelog.do_scrape(test_mode=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--start', type=int, required=True)
    parser.add_argument('-e', '--end', type=int, required=True)
    args = parser.parse_args()
    main(args)
