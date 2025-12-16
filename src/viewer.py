"""
Telemetry Viewer

This module reads logged telemetry data from the SQLite database and
provides tools for inspection and visualization.

It allows users to:
- View a sample of stored telemetry
- Query data within a specified time range
- Export queried data to CSV
- Plot telemetry channels over time
- Display a live-updating plot of recent telemetry

This module is used for analysis and visualization of logged data.
"""

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import sqlite3

#connect to database
conn = sqlite3.connect("data/telemetry.db")
cursor = conn.cursor()

query = """
SELECT timestamp, speed, fuel, rpm, lat, lon, throttle, temp FROM telemetry
ORDER BY timestamp ASC
LIMIT 200;
"""

cursor.execute(query)
rows = cursor.fetchall()

#prints first 200 rows
print("Showing first 200 rows:\n")
for row in rows:
    timestamp, speed, fuel, rpm, lat, lon, throttle, temp = row
    print(f"Time: {timestamp} | Speed: {speed} | Fuel: {fuel} | RPM: {rpm} | Location: Lat-{lat}, Lon-{lon} | Throttle: {throttle} | Temperature: {temp}")

#prompt for start and end time
start_str = input("Enter start time in ISO format(e.g.: 2025-12-17T11:21:43): ")
stop_str = input("Enter stop time in ISO format(e.g.: 2025-12-17T11:21:45): ")

try:
   start = pd.to_datetime(start_str)
   stop = pd.to_datetime(stop_str)
except ValueError:
    print("Invalid timestamp format. Enter correct time in ISO foemat (2025-12-17T11:21:45)")
    exit()

start_sql = start.isoformat()
stop_sql = stop.isoformat()

#query and print data
query2 = """
SELECT timestamp, speed, fuel, rpm, lat, lon, throttle, temp FROM telemetry
WHERE timestamp BETWEEN ? AND ?
ORDER BY timestamp ASC;
"""

cursor.execute(query2, (start_sql, stop_sql))
line = cursor.fetchall()

print(f"Telemetry from {start_sql} to {stop_sql}:\n")

for timestamp, speed, fuel, rpm, lat, lon, throttle, temp in line:
    print(f"Time: {timestamp} | Speed: {speed} | Fuel: {fuel} | RPM: {rpm} | Location: Lat-{lat}, Lon-{lon} | Throttle: {throttle} | Temperature: {temp}")

#option to export
df_range = pd.read_sql_query(query2, conn, params=(start_sql, stop_sql))
opt = input("Do you wish to export ranged telemtry values into CSV? (Y/N) ").lower()
if opt == 'y':
    df_range.to_csv("data/time_ranged_telemtry.csv", index=False)

#---------plot relevant telemetry with time----------
df = pd.read_sql_query("SELECT * FROM telemetry ORDER BY timestamp ASC", conn)


#convert timestamp
df["timestamp"] = pd.to_datetime(df["timestamp"])
df = df.sort_values("timestamp")

#--------plot speed-------
fig, ax = plt.subplots(5, 1, figsize=(10, 9), sharex=True)

ax[0].plot(df["timestamp"], df["speed"], color="blue")
ax[0].set_ylabel("Speed(km/h)")

#--------plot fuel-------
ax[1].plot(df["timestamp"], df["fuel"], color="black")
ax[1].set_ylabel("Fuel(%)")

#--------plot rpm-------
ax[2].plot(df["timestamp"], df["rpm"], color="purple")
ax[2].set_ylabel("RPM")

#--------plot throttle-------
ax[3].plot(df["timestamp"], df["throttle"], color="green")
ax[3].set_ylabel("Throttle%)")

#--------plot temp-------
ax[4].plot(df["timestamp"], df["temp"], color="red")
ax[4].set_ylabel("Temperature(C)")

plt.xlabel("Time(s)")
plt.tight_layout()
plt.savefig("data/telemetry_static_plot.png")
plt.show()

#add live mode that shows the latest 500 rows ad refreshes every 200ms

#create getting telemtry function
def get_recent_data():
    df2 = pd.read_sql_query("""
                            SELECT * FROM telemetry 
                            ORDER BY id DESC LIMIT 500
                            """, conn)

    df2["timestamp"] = pd.to_datetime(df2["timestamp"])
    return df2.sort_values("timestamp")

fig1, ax1 = plt.subplots()
line, = ax1.plot([],[])

def update(frame):
    df2 = get_recent_data()
    line.set_data(df2["timestamp"], df2["speed"])
    ax1.relim()
    ax1.autoscale_view()
    return line

anim = FuncAnimation(fig1, update, interval=200)

plt.show()

conn.close()