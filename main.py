import os
import logging

from obswebsocket import requests
from connection import ObsConnection
from time_util import get_time_by_start_stop, convert_date_time, get_current_time
from dotenv import load_dotenv

load_dotenv()

# ===== CONFIG =====
HOST = os.environ.get("HOST")
PORT = os.environ.get("PORT")
PASS = os.environ.get("PASS")
RECORD_DISPLAY = os.environ.get("RECORD_DISPLAY")


def main():
    logging.basicConfig(level=logging.INFO)

    start_time = get_time_by_start_stop(type="start")
    start_time = convert_date_time(*start_time)

    stop_time = get_time_by_start_stop(type="stop")
    stop_time = convert_date_time(*stop_time)

    time_now = get_current_time()

    logging.info(f"\nStart Recording at {start_time}")
    logging.info(f"Stop Recording at {stop_time}")
    logging.info(f"Current time: {time_now}\n")

    with ObsConnection(HOST, PORT, PASS) as client:
        # Will keep looping until current time is 
        # at start time
        while time_now < start_time:
            time_now = get_current_time()

        try:
            client.call(requests.StartRecording())
            logging.info("\nStart Recording...\n")
        except Exception as e:
            print(f"Exception {e}")

        # Will keep looping until current time is 
        # at stop time
        while time_now < stop_time:
            time_now = get_current_time()

        client.call(requests.StopRecording())
        logging.info("\nStop Recording...\n")

    # Shuts down computer
    logging.info("\nShutting down system...")
    os.system("shutdown /s /t 5")


if __name__ == "__main__":
    main()
