from dataclasses import dataclass
import requests
from bs4 import BeautifulSoup
import re
import time
import datetime
import json


# 参考: https://qiita.com/toshiyuki_tsutsui/items/f143946944a428ed105b
# 緯度経度取得: https://qiita.com/Kosuke0306Ikko/items/765589c329175364831b

@ dataclass
class Restaurant:
    store_id: str
    name: str
    latitude: str
    longitude: str
    review: list[str]


class Tabelog:
    """
    食べログスクレイピングクラス
    test_mode=Trueで動作させると、最初のページの３店舗のデータのみを取得できる
    """

    def __init__(self, base_url: str, review_num: int = 10, begin_page: int = 1, end_page: int = 10) -> None:

        # 変数宣言
        self.base_url = base_url
        self.store_id_num = 0
        self.review_num = review_num
        self.columns = ['store_id', 'store_name',
                        'score', 'ward', 'review_cnt', 'review']
        self.timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        self.begin_page = begin_page
        self.end_page = end_page
        self.__regexcomp = re.compile(r'\n|\s')  # \nは改行、\sは空白

    def do_scrape(self, test_mode: bool = True, ) -> None:

        page_num = self.begin_page  # 店舗一覧ページ番号

        if test_mode:
            # 食べログの点数ランキングでソートする際に必要な処理
            list_url = f"{self.base_url}{str(page_num)}/?Srt=D&SrtT=rt&sort_mode=1"

            restaurant_list = self.scrape_list(list_url, mode=test_mode)
        else:
            while True:
                # 食べログの点数ランキングでソートする際に必要な処理
                list_url = f"{self.base_url}{str(page_num)}/?Srt=D&SrtT=rt&sort_mode=1"
                print(
                    f"--------------finish_scripe page {page_num}---------------------")
                restaurant_list = self.scrape_list(list_url, mode=test_mode)
                if len(restaurant_list) == 0:
                    break
                self.dump_json(restaurant_list, page_num)
                # INパラメータまでのページ数データを取得する
                if page_num >= self.end_page:
                    break
                page_num += 1

    def scrape_list(self, list_url: str, mode: bool) -> list[Restaurant]:
        """
        店舗一覧ページのパーシング
        """
        r = requests.get(list_url)
        if r.status_code != requests.codes.ok:
            return False

        soup = BeautifulSoup(r.content, 'html.parser')
        soup_a_list = soup.find_all(
            'a', class_='list-rst__rst-name-target')  # 店名一覧

        if len(soup_a_list) == 0:
            return False

        restaurant_list = []
        if mode:
            for soup_a in soup_a_list[:2]:
                item_url = soup_a.get('href')  # 店の個別ページURLを取得
                self.store_id_num += 1
                restaurant = self.scrape_item(item_url)
                restaurant_list.append(restaurant)
        else:
            for soup_a in soup_a_list:
                item_url = soup_a.get('href')  # 店の個別ページURLを取得
                self.store_id_num += 1
                restaurant = self.scrape_item(item_url)
                restaurant_list.append(restaurant)

        return restaurant_list

    def scrape_item(self, item_url: str) -> Restaurant:
        """
        個別店舗情報ページのパーシング
        """
        start = time.time()

        r = requests.get(item_url)
        if r.status_code != requests.codes.ok:
            print(f'error:not found{ item_url }')
            return

        soup = BeautifulSoup(r.content, 'html.parser')

        # 店舗名称取得
        # <h2 class="display-name">
        #     <span>
        #         麺匠　竹虎 新宿店
        #     </span>
        # </h2>
        store_name_tag = soup.find('h2', class_='display-name')
        store_name = store_name_tag.span.string
        store_name = store_name.strip()
        print('{}→店名：{}'.format(self.store_id_num, store_name), end='')

        # ラーメン屋、つけ麺屋以外の店舗は除外
        store_head = soup.find(
            'div', class_='rdheader-subinfo')  # 店舗情報のヘッダー枠データ取得
        store_head_list = store_head.find_all('dl')
        store_head_list = store_head_list[1].find_all('span')
        #print('ターゲット：', store_head_list[0].text)

        if store_head_list[0].text not in {'ラーメン', 'つけ麺'}:
            print('ラーメンorつけ麺のお店ではないので処理対象外')
            self.store_id_num -= 1
            return

        # 評価点数取得
        # <b class="c-rating__val rdheader-rating__score-val" rel="v:rating">
        #    <span class="rdheader-rating__score-val-dtl">3.58</span>
        # </b>
        rating_score_tag = soup.find('b', class_='c-rating__val')
        rating_score = rating_score_tag.span.string

        # 評価点数が存在しない店舗は除外
        if rating_score == '-':
            print('  評価がないため処理対象外')
            self.store_id_num -= 1
            return
       # 評価が3.5未満店舗は除外
        if float(rating_score) < 3.5:
            print('  食べログ評価が3.5未満のため処理対象外')
            self.store_id_num -= 1
            return

        # レビュー一覧URL取得
        # <a class="mainnavi" href="https://tabelog.com/tokyo/A1304/A130401/13143442/dtlrvwlst/"><span>口コミ</span><span class="rstdtl-navi__total-count"><em>60</em></span></a>
        review_tag_id = soup.find('li', id="rdnavi-review")
        review_tag = review_tag_id.a.get('href')

        # レビュー一覧ページ番号
        page_num = 1  # 1ページ*20 = 20レビュー 。この数字を変えて取得するレビュー数を調整。

        # レビュー一覧ページから個別レビューページを読み込み、パーシング
        # 店舗の全レビューを取得すると、食べログの評価ごとにデータ件数の濃淡が発生してしまうため、
        # 取得するレビュー数は１ページ分としている（件数としては１ページ*20=２0レビュー）
        review = []
        while len(review) < self.review_num:
            review_url = review_tag + \
                'COND-0/smp1/?lc=0&rvw_part=all&PG=' + str(page_num)
            # print('\t口コミ一覧リンク：{}'.format(review_url))
            print(' . ', end='')  # LOG
            review_list = self.scrape_review(review_url)
            len_review_list = len(review_list)
            if len_review_list == 0:
                break
            page_num += 1
            review += review_list[:min(len_review_list,
                                       self.review_num - len_review_list)]

        ll = soup.find("script", {"type": "application/ld+json"}).string

        lat_st = ll.find("latitude")+10
        lat_ed = ll.find(",", lat_st)
        latitude = ll[lat_st:lat_ed]  # 店舗緯度取得

        lon_st = ll.find("longitude")+11
        lon_ed = ll.find("}", lon_st)
        longitude = ll[lon_st:lon_ed]  # 店舗経度取得

        process_time = time.time() - start
        print('  取得時間：{}'.format(process_time))
        restaurant = Restaurant(store_id=self.store_id_num, name=store_name,
                                latitude=latitude, longitude=longitude, review=review)

        return restaurant

    def scrape_review(self, review_url: str) -> list[str]:
        """
        レビュー一覧ページのパーシング
        """
        r = requests.get(review_url)
        if r.status_code != requests.codes.ok:
            print(f'error:not found{ review_url }')
            return []

        # 各個人の口コミページ詳細へのリンクを取得する
        # <div class="rvw-item js-rvw-item-clickable-area" data-detail-url="/tokyo/A1304/A130401/13141542/dtlrvwlst/B408082636/?use_type=0&amp;smp=1">
        # </div>
        soup = BeautifulSoup(r.content, 'html.parser')
        review_url_list = soup.find_all(
            'div', class_='rvw-item')  # 口コミ詳細ページURL一覧

        if len(review_url_list) == 0:
            return []
        review_list = []
        for url in review_url_list:
            review_detail_url = 'https://tabelog.com' + \
                url.get('data-detail-url')
            #print('\t口コミURL：', review_detail_url)

            # 口コミのテキストを取得
            review = self.get_review_text(review_detail_url)
            if not review:
                break
            review_list.append(review)

        return review_list

    def get_review_text(self, review_detail_url: str) -> str:
        """
        口コミ詳細ページをパーシング
        """
        r = requests.get(review_detail_url)
        if r.status_code != requests.codes.ok:
            print(f'error:not found{ review_detail_url }')
            return

        # ２回以上来訪してコメントしているユーザは最新の1件のみを採用
        # <div class="rvw-item__rvw-comment" property="v:description">
        #  <p>
        #    <br>すごい煮干しラーメン凪 新宿ゴールデン街本館<br>スーパーゴールデン1600円（20食限定）を喰らう<br>大盛り無料です<br>スーパーゴールデンは、新宿ゴールデン街にちなんで、ココ本店だけの特別メニューだそうです<br>相方と歌舞伎町のtohoシネマズの映画館でドラゴンボール超ブロリー を観てきた<br>ブロリー 強すぎるね(^^)面白かったです<br>凪の煮干しラーメンも激ウマ<br>いったん麺ちゅるちゅる感に、レアチャーと大トロチャーシューのトロけ具合もうめえ<br>煮干しスープもさすが！と言うほど完成度が高い<br>さすが食べログラーメン百名店<br>と言うか<br>2日連チャンで、近場の食べログラーメン百名店のうちの2店舗、昨日の中華そば葉山さんと今日の凪<br>静岡では考えられん笑笑<br>ごちそうさまでした
        #  </p>
        # </div>
        soup = BeautifulSoup(r.content, 'html.parser')
        # reviewが含まれているタグの中身をすべて取得
        review = soup.find_all('div', class_='rvw-item__rvw-comment')
        if len(review) == 0:
            review = ''
        else:
            review = review[0].p.text.strip()  # strip()は改行コードを除外する関数
        return review

    def dump_json(self, restaurant_list: list[Restaurant], page_num: int):
        restaurant_dict_list = []
        save_json_filename = f"../data/ramen_{page_num}.json"
        for restaurant in restaurant_list:
            try:
                restaurant_dict = vars(restaurant)
            except TypeError:
                print(f"can't to convert ot dict error: {restaurant}")
                continue
            restaurant_dict_list.append(restaurant_dict)
        with open(save_json_filename, 'w') as f:
            json.dump(restaurant_dict_list, f, ensure_ascii=False, indent=4)
