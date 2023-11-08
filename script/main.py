import psutil
import os
from datetime import datetime
import logging

import requests
from requests.exceptions import HTTPError, Timeout, ConnectionError



LOG_PATH = os.path.join(os.getcwd(), 'logfile.log')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s:%(levelname)s:%(message)s',
    filename=LOG_PATH,
    filemode='a'  
)


API_ENDPOINT = 'http://localhost:5000/companies'
VARIABLE_CONTROL = 40

def check_memory_usage():
    perc_virtual_mem = psutil.virtual_memory().percent 
    if perc_virtual_mem > VARIABLE_CONTROL:
        send_alarm(perc_virtual_mem)


def send_alarm(usage):
    current_time = datetime.now().isoformat()
    payload = {
        "data": f"Virtual memory equal {usage}",
        "event_time": current_time
    }
    try:
        requests.post(url=API_ENDPOINT, json=payload)
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

