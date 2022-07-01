from typing import Dict
import datetime


class Time:
    _MERIDIEMS = ["am", "pm"]
    _TIME_POSITIONS = ["start", "stop"]

    def __init__(self, time_pos: str):
        self.time_pos = time_pos
        self._inputted_time = self._get_time_from_input()
        self._time = self.time

    # TODO: method strategy: one for start stop time
    # one for video length
    def _get_time_from_input(self) -> Dict[str, str]:
        if self.time_pos not in self._TIME_POSITIONS:
            print("Provide valid type: start or stop")
            return None

        input_time = input(f"{self.time_pos.capitalize()} time: ") or None

        if self.time_pos == "stop" and input_time is None:
            print("Stop time must not be none")
            exit()

        if input_time is not None:
            input_time = self._parse_time_from_string(input_time)
            self._validate_time(input_time, time_pos=self.time_pos)

        return input_time

    @staticmethod
    def _parse_time_from_string(time: str) -> Dict[str, str]:
        if time is None:
            return None

        # 23 : 59 pm -> 23:59pm
        time = time.replace(" ", "")
        # 23:59pm -> [23, 59pm]
        time = time.split(":")

        hours, minutes = time
        meridiem = None

        if len(hours) not in range(1, 3):
            print("Invalid hours format given")
            exit()

        # if minutes is formatted like this due
        # to split method: 59pm
        if len(minutes) == 4:
            meridiem = minutes[-2:].lower()
            minutes = minutes[:2]

        if len(minutes) != 4 and len(minutes) != 2:
            print("Invalid minutes format given")
            exit()

        joined_time = ":".join([hours, minutes])
        time = {
            "hours": hours,
            "minutes": minutes,
            "meridiem": meridiem,
            "str_time": joined_time,
            "str_time_with_meridiem": f"{joined_time}{meridiem}" if meridiem else None,
        }

        return time

    @property
    def time(self) -> datetime.datetime:
        input_time = self._inputted_time
        now = datetime.datetime.now()

        if input_time is None:
            return now

        hour = input_time.get("hours")
        minute = input_time.get("minutes")
        meridiem = input_time.get("meridiem")

        today = datetime.datetime.today()
        year = today.year
        month = today.month
        day = today.day

        hour = int(hour) + 12 if meridiem == "pm" else int(hour)
        hour = 0 if hour == 12 and meridiem == "am" else hour
        minute = int(minute)

        self._time = datetime.datetime(year, month, day, hour, minute)

        if now > self._time:
            self._time = self._time.replace(day=day + 1)

        return self._time

    def _validate_meridiem(self, meridiem: str):
        if meridiem is None:
            return None

        if meridiem not in self._MERIDIEMS:
            print("Invalid meridiem given")
            exit()

    def _validate_time(self, time: dict, time_pos: str = "start"):
        # TODO: write tests
        # TODO: write custom exceptions

        if time_pos == "start" and time is None:
            return None

        hours = time.get("hours")
        minutes = time.get("minutes")
        meridiem = time.get("meridiem")

        self._validate_meridiem(meridiem)

        if int(hours) not in range(0, 24):
            print("Invalid hours format given")
            exit()

        if int(minutes) not in range(0, 60):
            print("Invalid minutes format given")
            exit()

        return True

    def __str__(self):
        return f"{self.time_pos} | {self.time}"


class RecordingStartTime(Time):
    def __init__(self):
        super().__init__("start")


class RecordingStopTime(Time):
    def __init__(self):
        super().__init__("stop")


class RecordViaLength:
    def __init__(self):
        self.start_time = datetime.datetime.now()
        self._recording_length = self._get_recording_length()
        self._stop_time = self.stop_time

    @property
    def stop_time(self):
        return self.start_time + self._time_at_video_length(*self._recording_length)

    def _get_recording_length(self) -> str:
        print(
            "\nFormat: [hours]:[minutes]:[seconds]:[milliseconds] (Optional: milliseconds)"
        )
        print("Example: 01:42:30:00 <- (1 hour 42 minutes 30 seconds)")
        recording_length = input("Recording length: ") or None
        recording_length = self._parse_recording_length(recording_length)

        return recording_length

    @staticmethod
    def _parse_recording_length(recording_length: str) -> Dict[str, int]:
        if recording_length is None:
            return (0, 0, 0, 0)

        if len(recording_length) not in range(8, 12):
            print(
                "Invalid Format | Format: [hours]:[minutes]:[seconds]:[milliseconds] (Optional: milliseconds)"
            )

        hrs, mins, secs, *ms = map(int, recording_length.split(":"))

        if len(ms) > 0:
            ms = ms[0]
        else:
            ms = 0

        return (hrs, mins, secs, ms)

    @staticmethod
    def _time_at_video_length(
        hours: int = 0,
        minutes: int = 0,
        seconds: int = 0,
        milliseconds: int = 0,
    ):
        return datetime.timedelta(
            hours=hours,
            minutes=minutes,
            seconds=seconds,
            milliseconds=milliseconds,
        )

    def __str__(self):
        return f"Start: {self.start_time} | Stop: {self.stop_time}"


def get_current_time():
    return datetime.datetime.now()
