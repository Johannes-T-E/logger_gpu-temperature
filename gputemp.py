import os
import time
import datetime

def get_gpu_temperature():
    try:
        # Command to get GPU temperature on Windows
        result = os.popen('nvidia-smi --query-gpu=temperature.gpu --format=csv,noheader').read().strip()
        # Convert temperature to integer
        gpu_temperature = int(result)
        return gpu_temperature
    except Exception as e:
        print("Error:", e)
        return None

def check_nvlddmkm_state():
    try:
        # Check if the "nvlddmkm.sys" file exists
        file_path = os.path.join(os.environ['SystemRoot'], 'System32', 'drivers', 'nvlddmkm.sys')
        if os.path.exists(file_path):
            return "Present"
        else:
            return "Not Present"
    except Exception as e:
        print("Error:", e)
        return None

def log_system_status(file_path):
    try:
        while True:
            # Get current timestamp
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            # Get GPU temperature
            gpu_temperature = get_gpu_temperature()
            if gpu_temperature is not None:
                # Get state of nvlddmkm.sys file
                nvlddmkm_state = check_nvlddmkm_state()
                # Log temperature and file state to file
                with open(file_path, 'a') as file:
                    file.write(f"{timestamp}, GPU Temperature: {gpu_temperature}°C, nvlddmkm.sys: {nvlddmkm_state}\n")
                print(f"{timestamp}, GPU Temperature: {gpu_temperature}°C, nvlddmkm.sys: {nvlddmkm_state}")
            # Wait for 60 seconds before logging again
            time.sleep(1)
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    log_file_path = "system_status_log.txt"
    log_system_status(log_file_path)
