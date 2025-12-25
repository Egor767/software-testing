import pandas as pd
import numpy as np
import sqlite3
from datetime import datetime, timedelta
import random

np.random.seed(42)
random.seed(42)


def generate_data(rows=1000, anomaly_rate=0.0):
    categories = ['Electronics', 'Clothing', 'Home', 'Books']
    weights = [0.7, 0.1, 0.1, 0.1] if anomaly_rate > 0 else [0.25, 0.25, 0.25, 0.25]

    data = {
        'transaction_id': range(1, rows + 1),
        'date': [datetime.now() - timedelta(days=x) for x in range(rows)],
        'category': np.random.choice(categories, rows, p=weights),
        'amount': np.random.uniform(10, 500, rows).round(2),
        'user_email': [f"user{i}@pmifi.ru" for i in range(rows)]
    }

    df = pd.DataFrame(data)

    if anomaly_rate > 0:
        df.loc[0:5, 'transaction_id'] = df.loc[6:11, 'transaction_id'].values
        df.loc[10:20, 'amount'] = df.loc[10:20, 'amount'] * -1
        df.loc[20:30, 'user_email'] = "invalid_email_format"
        df.loc[30:40, 'category'] = None

    return df


print("Генерация исторических данных (золотой набор)")
df_history = generate_data(rows=1000, anomaly_rate=0)
df_history.to_csv("historical_sales.csv", index=False)

print("Генерация продуктовых данных")
df_new = generate_data(rows=1500, anomaly_rate=1)
conn = sqlite3.connect("data/sales_warehouse.db")
df_new.to_sql("daily_sales", conn, if_exists="replace", index=False)
conn.close()
