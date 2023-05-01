from scrap_tabelog import Tabelog


def main():
    tokyo_ramen_review = Tabelog(
        base_url="https://tabelog.com/tokyo/rstLst/ramen/", test_mode=False, p_ward='東京都内')
    # CSV保存
    tokyo_ramen_review.df.to_csv("../data/tokyo_ramen_review.csv")


if __name__ == "__main__":
    main()
