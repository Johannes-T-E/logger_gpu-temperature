import os
import datetime
import logging
import argparse
import sqlite3
import time
from typing import Optional, Dict
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def get_gpu_temperature() -> Optional[int]:
    """
    Get the current GPU temperature using nvidia-smi.
    
    Returns:
        Optional[int]: GPU temperature in Celsius or None if error occurs
    """
    try:
        result = os.popen('nvidia-smi --query-gpu=temperature.gpu --format=csv,noheader').read().strip()
        return int(result) if result else None
    except Exception as e:
        logger.error(f"Error getting GPU temperature: {e}")
        return None

def init_database(db_path: str) -> None:
    """
    Initialize the SQLite database with the required table.
    
    Args:
        db_path (str): Path to the SQLite database file
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS gpu_temperatures (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME,
                temperature INTEGER
            )
        ''')
        conn.commit()
        conn.close()
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        raise

def log_temperature(db_path: str) -> Dict[str, any]:
    """
    Log GPU temperature to SQLite database and return the status data.
    
    Args:
        db_path (str): Path to the SQLite database file
        
    Returns:
        Dict[str, any]: Dictionary containing the logged GPU temperature
    """
    try:
        timestamp = datetime.datetime.now()
        gpu_temp = get_gpu_temperature()
        
        if gpu_temp is not None:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO gpu_temperatures (timestamp, temperature) VALUES (?, ?)',
                (timestamp, gpu_temp)
            )
            conn.commit()
            conn.close()
            
            logger.info(f"GPU Temperature: {gpu_temp}°C")
            
        return {
            'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'gpu_temperature': gpu_temp
        }
        
    except Exception as e:
        logger.error(f"Error logging temperature to database: {e}")
        raise

def monitor_temperature(db_path: str, interval_ms: int, duration_seconds: int) -> None:
    """
    Monitor GPU temperature at specified intervals for a specified duration.
    
    Args:
        db_path (str): Path to the SQLite database file
        interval_ms (int): Time between measurements in milliseconds
        duration_seconds (int): Total monitoring duration in seconds
    """
    try:
        start_time = time.time()
        end_time = start_time + duration_seconds
        
        logger.info(f"Starting temperature monitoring for {duration_seconds} seconds with {interval_ms}ms intervals")
        
        while time.time() < end_time:
            log_temperature(db_path)
            time.sleep(interval_ms / 1000)  # Convert milliseconds to seconds
            
        logger.info("Temperature monitoring completed")
        
    except KeyboardInterrupt:
        logger.info("Temperature monitoring stopped by user")
    except Exception as e:
        logger.error(f"Error during temperature monitoring: {e}")
        raise

def query_temperatures(db_path: str, limit: int = 10) -> None:
    """
    Query and display recent temperature readings from the database.
    
    Args:
        db_path (str): Path to the SQLite database file
        limit (int): Number of recent readings to display
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT timestamp, temperature 
            FROM gpu_temperatures 
            ORDER BY timestamp DESC 
            LIMIT ?
        ''', (limit,))
        
        results = cursor.fetchall()
        conn.close()
        
        if results:
            logger.info(f"\nLast {limit} temperature readings:")
            for timestamp, temp in results:
                logger.info(f"{timestamp}: {temp}°C")
        else:
            logger.info("No temperature readings found in database")
            
    except Exception as e:
        logger.error(f"Error querying temperatures: {e}")
        raise

def main():
    parser = argparse.ArgumentParser(description='GPU Temperature Logger')
    parser.add_argument('--db-file', default='gpu_temperatures.db',
                      help='Path to the SQLite database file')
    parser.add_argument('--query', action='store_true',
                      help='Query recent temperature readings instead of logging')
    parser.add_argument('--limit', type=int, default=10,
                      help='Number of recent readings to display when querying')
    parser.add_argument('--monitor', action='store_true',
                      help='Monitor temperature at specified intervals')
    parser.add_argument('--interval', type=int, default=1000,
                      help='Time between measurements in milliseconds (default: 1000ms)')
    parser.add_argument('--duration', type=int, default=60,
                      help='Total monitoring duration in seconds (default: 60s)')
    
    args = parser.parse_args()
    
    try:
        # Initialize database if it doesn't exist
        init_database(args.db_file)
        
        if args.query:
            query_temperatures(args.db_file, args.limit)
        elif args.monitor:
            monitor_temperature(args.db_file, args.interval, args.duration)
        else:
            log_temperature(args.db_file)
            
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        raise

if __name__ == "__main__":
    main()
