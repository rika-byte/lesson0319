import requests
import pandas as pd

REQUEST_URL = "https://app.rakuten.co.jp/services/api/Travel/SimpleHotelSearch/20170426"
APP_ID = "1051925217941905423"

# パラメータ設定
params = {
    'format':'json',
    'largeClassCode': 'japan',
    'middleClassCode': 'okinawa',
    'smallClassCode': 'nahashi',
    'applicationId': APP_ID    
}

# requestsのgetメソッドを使ってアクセス
# その結果をresに代入します。
res = requests.get(REQUEST_URL, params=params)

# 欲しいデータはresのjsonに格納されているので、res.json()をresultに代入しておきましょう。
result = res.json()
# これでAPIで取得したデータはresultに代入されます。

# ホテル情報のリストを取得
hotels = result.get("hotels", [])

# 必要な情報を抽出してリストに格納
hotel_list = []
for hotel in hotels:
    info = hotel["hotel"][0]["hotelBasicInfo"]
    hotel_list.append({
        "hotel_name": info["hotelName"],
        "address": info["address1"] + info["address2"],
        "review_score": info.get("reviewAverage", None),  # 評価点（ない場合はNone）
        "review_count": info.get("reviewCount", 0),  # レビュー数（ない場合は0）
        "min_price": info.get("hotelMinCharge", None)  # 最低価格（ない場合はNone）
    })

# Pandasのデータフレームに変換
df = pd.DataFrame(hotel_list)

# データの確認
print(df.head())

import plotly.express as px

# レビュー数が多い順に並べる
df_sorted = df.sort_values(by="review_count", ascending=False).head(10)

# グラフ作成
fig = px.bar(df_sorted, x="hotel_name", y="review_count", 
             title="レビュー数が多いホテル", text="review_count")

# グラフを表示
fig.show()

import streamlit as st

st.title("楽天トラベル ホテル検索ダッシュボード")

# ユーザーが選択できるセレクトボックス
selected_hotel = st.selectbox("ホテルを選択してください", df["hotel_name"])

# 選択されたホテルのデータを取得
selected_data = df[df["hotel_name"] == selected_hotel]

# ホテル情報を表示
st.write("### ホテル情報")
st.dataframe(selected_data)

# グラフを表示
st.write("### ホテルのレビュー数ランキング")
st.plotly_chart(fig)
