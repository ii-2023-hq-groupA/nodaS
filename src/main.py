from scrap_tabelog import Tabelog

BASE_URL = "https://tabelog.com/tokyo/rstLst/ramen/"

def main():
    tabelog = Tabelog(
        base_url=BASE_URL, p_ward='文京区')
    tabelog.do_scrape(test_mode=True)


if __name__ == "__main__":
    main()
