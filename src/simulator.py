"""
Telemetry Simulator

This module simulates realistic vehicle telemetry data.

It runs a TCP server that streams telemetry packets as JSON strings at fixed
time intervals. Each packet represents the current state of the simulated
vehicle and ends with a newline character for safe transmission.

This simulator is the data source for the logger module.
"""

#import relevant modules
import socket
import time
import json
import random
from datetime import datetime

#iniialize data/values
speed = 0
fuel = 100
lat = 3.2367
lon = 5.8723
rpm = 0
throttle = 0
temp = 20

#function to create json packets
def generate_packet():
    """
Generate a single telemetry packet with realistic vehicle behavior.
Speed, RPM, fuel, and temperature drift smoothly over time.
"""
    global speed, fuel, rpm, lat, lon, throttle, temp

    #---------update values----------
    
    #update speed smoot drift
    change_speed = random.randint(-2, 3)
    speed += change_speed
    speed = max(0, min(speed, 200 ))
    
    #decrease fuel(small burn rate)
    fuel = max(0, fuel - random.uniform(0.01, 0.05))
    
    #slight location drift
    loc_change = random.uniform(-0.0001, 0.0001)
    lat += loc_change
    lon += loc_change
    
    #steadily increase or decrease revolution
    rev_change = random.randint(-50, 100)
    rpm += rev_change
    rpm = max(800, min(rpm, 6000))
    
    #steady thtottle percentage drift
    throttle_change = random.randint(-5, 5)
    throttle += throttle_change
    throttle = max(0, min(throttle, 100)  )
    
    #slight temperature change
    temp_change = random.uniform(-0.2, 0.5)
    temp += temp_change
    temp = max(20, min(temp, 100))

    data = {
        #define global values
        "speed" : round(speed, 2),
        "fuel": round(fuel, 2),
        "location": {
        "lat": round(lat, 6),
        "lon": round(lon, 6),
        },
        "rpm": round(rpm, 2),
        "throttle": throttle,
        "temp":round(temp, 2),
        "timestamp": datetime.utcnow().isoformat()
    }
    return data

#create socket, bind and listen
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 9000))
server.listen(1)

while True:
    #connect to client
    print("Establishing connection...")
    conn, addr = server.accept()
    print("Connection secured! Address: ", addr)
    try:
        #Loop to send packet at 100ms interval
        while True:
            packet = generate_packet()
            message = json.dumps(packet) + "\n"
            conn.sendall(message.encode("utf-8"))
            time.sleep(0.1)

    except (BrokenPipeError, ConnectionResetError):
        print("Client Diconnected.")
    
    finally:
        conn.close()
