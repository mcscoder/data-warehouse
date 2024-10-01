from sqlalchemy import create_engine
import pandas as pd

df = pd.read_csv("weather_data.csv")

df["Date_Time"] = pd.to_datetime(df["Date_Time"])  # Chuyển đổi sang datetime
df["year"] = df["Date_Time"].dt.year
df["month"] = df["Date_Time"].dt.month
df["day"] = df["Date_Time"].dt.day
df["hour"] = df["Date_Time"].dt.hour

date_dim = (
    df[["Date_Time", "year", "month", "day", "hour"]]
    .drop_duplicates()
    .reset_index(drop=True)
)
date_dim["date_id"] = date_dim.index + 1  # Tạo khóa chính cho bảng Date_Dim

location_dim = df[["Location"]].drop_duplicates().reset_index(drop=True)
location_dim["location_id"] = (
    location_dim.index + 1
)  # Tạo khóa chính cho bảng Location_Dim

# Merge dữ liệu từ Date_Dim và Location_Dim vào bảng chính
df = df.merge(date_dim[["Date_Time", "date_id"]], on="Date_Time", how="left")
df = df.merge(location_dim[["Location", "location_id"]], on="Location", how="left")

# Tạo bảng fact
weather_fact = df[
    [
        "date_id",
        "location_id",
        "Temperature_C",
        "Humidity_pct",
        "Precipitation_mm",
        "Wind_Speed_kmh",
    ]
]

# Tạo kết nối đến MySQL
engine = create_engine("mysql://root:mcs@localhost/weather_db")

# Nạp dữ liệu vào các bảng
date_dim.to_sql("Date_Dim", con=engine, if_exists="replace", index=False)
location_dim.to_sql("Location_Dim", con=engine, if_exists="replace", index=False)
weather_fact.to_sql("Weather_Fact", con=engine, if_exists="replace", index=False)
