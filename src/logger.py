"""
Telemetry Logger

This module connects to the telemetry simulator over TCP and receives
streamed JSON telemetry packets.

It buffers incoming data, reconstructs complete packets, decodes them,
and stores the telemetry in both a CSV file and an SQLite database.

The logger also provides basic live monitoring by printing every
Nth packet to the console.
"""

#import necessary modules
import socket
import json
import csv
import sqlite3

#database setup
conn = sqlite3.connect("telemetry.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS telemetry(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        speed REAL,
        rpm REAL,
        fuel REAL,
        lat REAL,
        lon REAL,
        throttle REAL,
        temp REAL
);
""")

#create client and connect to simulator
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("localhost", 9000))

#create buffer
buffer = ""

#create csv
csv_file = open("vehicle-data-logger/data/telemetry_log.csv", "w", newline="")
writer = csv.DictWriter(csv_file, fieldnames=["speed", "rpm", "fuel","lat", "lon", "throttle", "temp", "timestamp"])
writer.writeheader()

# initialize packet counting
packet_count = 0

#
print_every = 50    #prints every N packet
max_prints = 5      #stop after this many attempts
print_count = 0     #how many times we've printed so far
preview_done = False


#recieve raw json bytes and decode
while True:
    try:
        data = client.recv(1024).decode()
        if not data:
            raise ConnectionError("Server Disconnected.")
    except ConnectionError:
        print("Lost Connection. Reconnecting")
    buffer += data

    while "\n" in buffer:
        line, buffer = buffer.split("\n", 1)

        if line.strip() == "":
            continue

        try:
            #convert packet to dictionary
            packet = json.loads(line)

            if packet == None:
                continue

            lat = packet["location"]["lat"]
            lon = packet["location"]["lon"]

            flat_packet = {
                "timestamp": packet["timestamp"],
                "speed" : packet["speed"],
                "rpm" : packet["rpm"],
                "fuel" : packet["fuel"],
                "lat": lat,
                "lon" : lon,
                "throttle" : packet["throttle"],
                "temp" : packet["temp"]
            }

            packet_count += 1

            #print 50th packet
            if packet_count % print_every == 0 and print_count < max_prints:
                print_count += 1

                print(
                    f"[{packet_count}]"
                    f"Speed ={flat_packet['speed']} km/h, "
                    f"RPM ={flat_packet['rpm']}, "
                    f"Fuel ={flat_packet['fuel']} %, "
                    f"Latitude ={flat_packet['lat']}, "
                    f"Longitude ={flat_packet['lon']}, "
                    f"Throttle ={flat_packet['throttle']} %, "
                    f"Temperature ={flat_packet['temp']} C, "
                    )

            if print_count == max_prints and not preview_done:
                print("Live telemetry preview complete. Logging will continue silently.")
                preview_done = True

            #write to csv
            writer.writerow(flat_packet)
            csv_file.flush()

            #write to sql
            cursor.execute("""
                INSERT INTO telemetry (timestamp, speed, rpm, fuel, lat, lon, throttle, temp)
                VALUES(?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    flat_packet["timestamp"], 
                    flat_packet["speed"], 
                    flat_packet["rpm"], 
                    flat_packet["fuel"], 
                    flat_packet["lat"],
                    flat_packet["lon"], 
                    flat_packet["throttle"], 
                    flat_packet["temp"],
                ))
            
            conn.commit()

        except json.JSONDecodeError:
            pass