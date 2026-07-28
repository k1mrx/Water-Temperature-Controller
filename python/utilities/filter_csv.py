import pandas as pd
import numpy as np
from scipy.signal import savgol_filter



csv_name = input('enter the csv file name that you want fitler (without .csv!!)):\n')
output_csv = csv_name + '_filtered.csv'

time_col = "time"


window_length = 21   # should be an odd number
polyorder = 2


df = pd.read_csv(csv_name + '.csv')


if window_length >= len(df):
    raise ValueError("window_length is longer than length of data")

if window_length % 2 == 0:
    raise ValueError("window_length should be odd")

# filtering
temp_raw = df['temperature'].values

temp_filtered = savgol_filter(
    temp_raw,
    window_length=window_length,
    polyorder=polyorder
)

# add filtered data to csv file
df["temperature_filtered"] = temp_filtered


df.to_csv(output_csv, index=False)

print("Filtered CSV saved as:", output_csv)
