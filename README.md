# Vehicle Telemetry Simulator & Data Logger

## Overview

This project is a **Python-based Vehicle Telemetry Simulator, Data Logger, and Visualization system** designed to model how real-world vehicle sensor data is generated, transmitted, stored, and analyzed.

It simulates live vehicle telemetry (speed, RPM, throttle, fuel level, temperature, and GPS coordinates), logs the data into a CSV file and an SQLite database, and provides tools for querying, exporting, and visualizing that data both statically and in near real-time.

The project was built as a **capstone-style learning project** after several months of structured Python study, with a focus on writing clear, maintainable, and industry-aligned code relevant to **transportation systems, aviation operations, and engineering data analysis**.

---

## Why This Project Matters

Modern transportation systems — including **airport ground vehicles, airside operations equipment, and fleet systems** — rely heavily on telemetry data for:

* Monitoring vehicle health and usage
* Fuel efficiency tracking
* Operational safety and compliance
* Data-driven maintenance decisions

This project demonstrates practical understanding of how such systems are architected end-to-end:
**data generation → networking → persistence → analysis → visualization**.

---

## Key Features

### 1. Vehicle Telemetry Simulator

* Generates realistic vehicle sensor data at fixed time intervals
* Parameters include:

  * Speed (km/h)
  * Engine RPM
  * Throttle position (%)
  * Fuel level (%)
  * Engine temperature (°C)
  * GPS latitude & longitude
* Uses bounded, incremental changes to mimic real vehicle behavior

### 2. Data Logging System

* Telemetry is stored in an **SQLite database**
* Timestamped records for accurate time-series analysis
* Designed to be lightweight, reliable, and easy to extend

### 3. Telemetry Viewer & Analyzer

* View recent telemetry samples directly from the database
* Query telemetry within a specific time range
* Export queried data to CSV for further analysis
* Generate static multi-channel plots (speed, fuel, RPM, throttle, temperature)
* Live-updating plots that refresh at fixed intervals

### 4. Clean & Modular Architecture

* Clear separation of concerns:

  * `simulator.py` → data generation
  * `logger.py` → data reception & storage
  * `viewer.py` → analysis & visualization
* Code written with readability, documentation, and maintainability in mind

---

## Technologies Used

* **Python 3**
* **SQLite** (local relational database)
* **Pandas** (data handling & analysis)
* **Matplotlib** (visualization & live plotting)
* **Socket Programming** (telemetry transmission)

---

## Project Structure

```
vehicle-data-logger/
│
├── src/
│   ├── simulator.py      # Generates live vehicle telemetry
│   ├── logger.py         # Receives and stores telemetry in SQLite
│   └── viewer.py         # Queries, exports, and visualizes telemetry
│
├── data/
│   ├── telemetry.db      # SQLite database
│   ├── telemetry_static_plot.png
│   └── time_ranged_telemetry.csv
│
├── README.md
└── .gitignore
```

---

## How to Run the Project

1. Clone the repository

```bash
git clone <repository-url>
cd vehicle-data-logger
```

2. Start the logger

```bash
python src/logger.py
```

3. Start the simulator (in a new terminal)

```bash
python src/simulator.py
```

4. Run the viewer

```bash
python src/viewer.py
```

---

## Example Use Cases

* Simulating ground vehicle telemetry for airport operations
* Learning how telemetry pipelines are built and analyzed
* Practicing time-series data visualization
* Demonstrating applied Python skills for engineering internships

---

## Skills Demonstrated

* Python programming fundamentals and best practices
* Data modeling and persistence with SQLite
* Time-series data analysis
* Data visualization and reporting
* Modular software design
* Debugging and incremental system development

---

## Future Improvements

* Support for multiple simulated vehicles
* Configurable telemetry profiles (airport buses, tugs, service vehicles)
* REST or WebSocket-based telemetry streaming
* Dashboard-style visualization
* Alerting for abnormal telemetry values

---

## About the Author

This project was developed as part of a structured learning journey in Python and data engineering, with a strong interest in **transportation systems, aviation operations, and engineering technology**.

It is intended as a practical demonstration of readiness for **internship-level technical roles** involving data analysis, systems monitoring, or engineering support.

---

## License

This project is licensed under the MIT License.
