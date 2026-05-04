# ISS Tracking Data Logger

A small Python automation project that retrieves the real-time position of the International Space Station using a public API, checks whether it is near a predefined user location, logs each execution step, and stores timestamped tracking data in a CSV file using Pandas.

## Features

- Retrieves real-time ISS location data from a public REST API
- Parses JSON responses and extracts latitude/longitude coordinates
- Compares the ISS position with a predefined user location
- Logs execution events in a text file
- Stores timestamped tracking data in a CSV file using Pandas
- Includes SMTP email alerting logic for when the ISS is near the selected location

## Technologies Used

- Python
- Requests
- Pandas
- REST API
- JSON
- CSV
- SMTP
- Logging

## Project Structure

```text
iss-tracking-data-logger/
│
├── main.py
├── README.md
├── .gitignore
├── sample_iss_tracking_data.csv
└── sample_code_log.txt
