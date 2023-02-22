import numpy as np
import pandas as pd
import datetime as dt
df_ = pd.read_csv("flo_data_20k.csv")
df = df_.copy()
pd.set_option("display.max_rows",20)
pd.set_option("display.max_columns",None)
pd.set_option("display.width", 500)
df.head(10)
df.columns
df.dtypes
df.describe().T
df.isnull().sum()
df["order_num_total"] = df["order_num_total_ever_online"] + df["order_num_total_ever_offline"]
df["customer_value_total"] = df["customer_value_total_ever_offline"] + df["customer_value_total_ever_online"]
date_columns = df.columns[df.columns.str.contains("date")]
df[date_columns] = df[date_columns].apply(pd.to_datetime)
df.info()
df.groupby('order_channel').agg({ "master_id": "count",
                                  "order_num_total": "sum",
                                  "customer_value_total": "sum"})
df.sort_values(by='customer_value_total', ascending=False)[:10]

# recency, frequency, monetary metriklerinin bulunması
rfm = pd.DataFrame()
df["last_order_date"].max()
today_date = dt.datetime(2021,6,1)
rfm['recency'] = (today_date - df["last_order_date"]).astype('timedelta64[D]')
rfm["frequency"] = df["order_num_total"]
rfm["monetary"] = df["customer_value_total"]


# RFM SKORLARININ BULUNMASI
rfm["recency_score"] = pd.qcut(rfm["recency"],5 , labels= [5,4,3,2,1])
rfm["frequency_score"] = pd.qcut(rfm["frequency"].rank(method="first"), 5,labels = [1,2,3,4,5])
rfm["monetary_score"] = pd.qcut(rfm["monetary"],5 , labels=[1,2,3,4,5])

rfm["RF_SCORE"] = (rfm["recency_score"].astype(str) + rfm["frequency_score"].astype(str))

seg_map = {
    r'[1-2][1-2]': "hibernating",
    r'[1-2][3-4]': "at_Risk",
    r'[1-2]5': "cant_loose",
    r'3[1-2]': "about_to_sleep",
    r'33': "need_attention",
    r'[3-4][4-5]': "loyal_customers",
    r'41': "promising",
    r'51': "new_customers",
    r'[4-5][2-3]': "potential_loyalists",
    r'5[4-5]': "champions"
}
rfm["segment"] = rfm["RF_SCORE"].replace(seg_map, regex =True)

# 2. RFM analizi yardımı ile 2 case için ilgili profildeki müşterileri bulunuz ve müşteri id'lerini csv ye kaydediniz.

# a. FLO bünyesine yeni bir kadın ayakkabı markası dahil ediyor. Dahil ettiği markanın ürün fiyatları genel müşteri tercihlerinin üstünde. Bu nedenle markanın
# tanıtımı ve ürün satışları için ilgilenecek profildeki müşterilerle özel olarak iletişime geçeilmek isteniliyor. Bu müşterilerin sadık  ve
# kadın kategorisinden alışveriş yapan kişiler olması planlandı. Müşterilerin id numaralarını csv dosyasına yeni_marka_hedef_müşteri_id.cvs
# olarak kaydediniz.
rfm["customer_id"] = df["master_id"]
target_segments_customer_ids = rfm[rfm["segment"].isin(["champions","loyal_customers"])]["customer_id"]
cust_ids = df[(df["master_id"].isin(target_segments_customer_ids)) &(df["interested_in_categories_12"].str.contains("KADIN"))]["master_id"]
cust_ids.to_csv("customer_ID.csv")
# b. Erkek ve Çoçuk ürünlerinde %40'a yakın indirim planlanmaktadır. Bu indirimle ilgili kategorilerle ilgilenen geçmişte iyi müşterilerden olan ama uzun süredir
# alışveriş yapmayan ve yeni gelen müşteriler özel olarak hedef alınmak isteniliyor. Uygun profildeki müşterilerin id'lerini csv dosyasına indirim_hedef_müşteri_ids.csv
# olarak kaydediniz.
target_segments_customer_ids_2 = rfm[rfm["segment"].isin(["cant_loose","hibernating","new_costumers"])]['customer_id']
cust_ids_2 = df[(df["master_id"].isin(target_segments_customer_ids_2)) & ((df["interested_in_categories_12"].str.contains("ERKEK")) |( df["interested_in_categories_12"].str.contains("COCUK")))]["master_id"]
cust_ids_2.to_csv("customer_ID_2'.csv")