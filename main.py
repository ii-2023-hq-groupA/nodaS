from src.scrap_tabelog import Tabelog
import argparse

BASE = "C13101"
# A1301 ~ A1331 が　東京の地域別
# C13101 ~ C13123 が　東京の23区
# Rから始まるのは路線別  e.g. 山手線=R9、日比谷線=R1096)

def main(args):
    print(f"search : begin: {args.start} -> end: {args.end}")
    tabelog = Tabelog(base=BASE, rating=args.rating,
                      begin_page=args.start, end_page=args.end)
    tabelog.do_scrape(test_mode=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--rating', type=int, required=True)
    parser.add_argument('-s', '--start', type=int, required=True)
    parser.add_argument('-e', '--end', type=int, required=True)
    args = parser.parse_args()
    main(args)
