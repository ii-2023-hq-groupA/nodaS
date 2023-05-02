# ラーメン

## スクレイピング

### 実行方法

`python main.py -s <startページ数> -e <endページ数>`

### データ

`data/`に格納されていきます．

- json ファイル名: `ramen_<ページ数>.json`

## 味データ処理

### 実行方法

`pyhton src/count_taste.py`

- data ディレクトリ内に全ての json データを格納しておく.

### データ

- `analysis_data/ramen_count_taste.csv`に格納されています．
