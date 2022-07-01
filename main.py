import os
import logging

from obswebsocket import requests
from connection import ObsConnection
from dotenv import load_dotenv

from time_util import (
    RecordingStartTime,
    RecordingStopTime,
    RecordViaLength,
    get_current_time,
)

load_dotenv()

# ===== CONFIG =====
HOST = os.environ.get("HOST")
PORT = os.environ.get("PORT")
PASS = os.environ.get("PASS")
RECORD_DISPLAY = os.environ.get("RECORD_DISPLAY")

AFFIRMATIVE_WORDS = ["yes", "y"]
NEGATIVE_WORDS = ["no", "n"]


def main():
    logging.basicConfig(level=logging.INFO)

    time_now = get_current_time()

    print("\nDo you want to record via length instead of start/stop times?")
    record_via_length = input("Record via length [yes/no]: ")

    if record_via_length.lower() in AFFIRMATIVE_WORDS:
        record_time = RecordViaLength()
        start_time = record_time.start_time
        stop_time = record_time.stop_time
    elif record_via_length.lower() in NEGATIVE_WORDS:
        start_rec = RecordingStartTime()
        start_time = start_rec.time
        stop_rec = RecordingStopTime()
        stop_time = stop_rec.time

    shutdown_comp = shutdown_query()

    print("")
    logging.info(f" Start Recording | {start_time}")
    logging.info(f" Stop Recording  | {stop_time}")
    logging.info(f" Current time    | {time_now}\n")

    with ObsConnection(HOST, PORT, PASS) as client:
        loop_until(start_time)

        try:
            client.call(requests.StartRecording())
            logging.info(" Start Recording...\n")
        except Exception as e:
            print(f"Exception {e}")

        loop_until(stop_time)

        client.call(requests.StopRecording())
        logging.info(" Stop Recording...\n")

    if shutdown_comp:
        computer_shut_down()


def loop_until(set_time):
    # Will keep looping until current time is
    # at set time
    time_now = get_current_time()
    while time_now < set_time:
        time_now = get_current_time()

    return


def shutdown_query():
    print("\nDo you want to shutdown your computer after recording?")
    queries = [
        "Shutdown after recording? [yes/no]: ",
        "Are you sure? [yes/no]: ",
    ]

    for i in range(2):
        shutdown_comp = input(f"{queries[i]}")
        if shutdown_comp.lower() in AFFIRMATIVE_WORDS:
            continue
        elif shutdown_comp.lower() in NEGATIVE_WORDS:
            print("Your computer will not shutdown after recording...\n")
            return False
        else:
            print("Invalid entry.\n")
            exit()

    shutdown_comp = True
    print("Your computer will shutdown after recording...\n")

    return shutdown_comp


def computer_shut_down():
    print("\nShutting down system...")
    os.system("shutdown /s /t 5")

    return


if __name__ == "__main__":
    main()
