# GPU Temperature Monitor

A Python script to monitor and log NVIDIA GPU temperatures using `nvidia-smi`. The script can take single measurements or monitor temperatures over time, storing the data in an SQLite database.

## Features

- Single temperature measurements
- Continuous monitoring with configurable intervals
- SQLite database storage for historical data
- Query recent temperature readings
- Configurable monitoring duration and intervals
- Detailed logging

## Requirements

- Python 3.6 or higher
- NVIDIA GPU with drivers installed
- `nvidia-smi` command-line tool (comes with NVIDIA drivers)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/gpu-temperature-monitor.git
cd gpu-temperature-monitor
```

2. (Optional) Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

## Usage

### Basic Usage

Take a single temperature measurement:
```bash
python gputemp.py
```

### Monitoring Mode

Monitor temperature every second for 60 seconds (default):
```bash
python gputemp.py --monitor
```

Monitor temperature with custom interval and duration:
```bash
python gputemp.py --monitor --interval 500 --duration 30
```

### Query Mode

View the last 10 temperature readings (default):
```bash
python gputemp.py --query
```

View a custom number of recent readings:
```bash
python gputemp.py --query --limit 20
```

### Custom Database Location

Specify a custom database file location:
```bash
python gputemp.py --db-file "custom_location.db"
```

## Command Line Arguments

- `--db-file`: Path to the SQLite database file (default: 'gpu_temperatures.db')
- `--query`: Query recent temperature readings instead of logging
- `--limit`: Number of recent readings to display when querying (default: 10)
- `--monitor`: Enable monitoring mode
- `--interval`: Time between measurements in milliseconds (default: 1000ms)
- `--duration`: Total monitoring duration in seconds (default: 60s)

## Database Schema

The SQLite database uses the following schema:
```sql
CREATE TABLE gpu_temperatures (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME,
    temperature INTEGER
)
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Uses `nvidia-smi` for GPU temperature monitoring
- Built with Python's standard library 