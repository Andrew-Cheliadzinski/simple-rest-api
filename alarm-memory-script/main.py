import os
import logging
import psutil
from datetime import datetime
import requests
from requests.exceptions import HTTPError, Timeout, ConnectionError


LOG_PATH = os.path.join(os.getcwd(), 'logfile.log')
API_ENDPOINT = 'http://localhost:8080/memory'
MEMORY_THRESHOLD = 40


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s:%(levelname)s:%(message)s',
    filename=LOG_PATH,
    filemode='a'  
)


def check_memory_usage():
    memory_usage = psutil.virtual_memory().percent 
    if memory_usage > MEMORY_THRESHOLD:
        send_alarm(memory_usage)


def send_alarm(usage):
    
    payload = {
        "data": f"Virtual memory equal {usage}",
        "event_time": datetime.now().isoformat()
    }
    try:
        response = requests.post(url=API_ENDPOINT, json=payload)
        response.raise_for_status()
    except HTTPError as http_err:
        logging.error(f"HTTP error occurred: {http_err}")
    except Timeout as timeout_err:
        logging.error(f"Timeout error occurred: {timeout_err}")
    except ConnectionError as conn_err:
        logging.error(f"Connection error occurred: {conn_err}")
    except Exception as err:
        logging.error(f"An error occurred: {err}")

    

if __name__ == "__main__":
    check_memory_usage()

