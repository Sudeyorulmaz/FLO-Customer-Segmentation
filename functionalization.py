import pandas as pd
import numpy as np
import datetime as dt
def data_preparation(dataframe):
    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", 500)
    dataframe.isnull().sum()
    dataframe["order_num_total"] = dataframe["order_num_total_ever_online"] + dataframe["order_num_total_ever_offline"]
    dataframe["customer_value_total"] = dataframe["customer_value_total_ever_offline"] + dataframe["customer_value_total_ever_online"]
    date_columns = dataframe.columns[dataframe.columns.str.contains("date")]
    dataframe[date_columns] = dataframe[date_columns].apply(pd.to_datetime)
    return dataframe



data_preparation(df)