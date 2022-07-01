import datetime

MERIDIEMS = ["am", "pm"]

# TODO: add type hints
# TODO: method strategy: one for start stop time
# one for video length
def get_time_by_start_stop(type: str = "start"):
    if type not in ["start", "stop"]:
        print("Provide valid type: start or stop")
        return None

    time = input(f"{type.capitalize()} time: ") or None
    meridiem = None

    if type == "stop" and time is None:
        print("Stop time must not be none")
        exit()

    if time is not None:
        time = parse_time_from_string(time)
        validate_time(time, type=type)

    return time, meridiem


def parse_time_from_string(time: str):
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


def validate_meridiem(meridiem: str):
    if meridiem is None:
        return None

    if meridiem not in ["am", "pm"]:
        print("Invalid meridiem given")
        exit()


def validate_time(time: dict, type: str = "start"):
    # TODO: write tests
    # TODO: write custom exceptions

    if type == "start" and time is None:
        return None, None

    hours = time.get("hours")
    minutes = time.get("minutes")
    meridiem = time.get("meridiem")

    validate_meridiem(meridiem)

    if int(hours) not in range(0, 24):
        print("Invalid hours format given")
        exit()

    if int(minutes) not in range(0, 60):
        print("Invalid minutes format given")
        exit()

    return True


def convert_date_time(time: dict):
    # TODO: implement code if time is none and type is start (means get current time)
    hour = time.get("hours")
    minute = time.get("minutes")
    meridiem = time.get("meridiem")

    today = datetime.datetime.today()
    year = today.year
    month = today.month
    day = today.day

    hour = int(hour) + 12 if meridiem == "pm" else int(hour)
    hour = 0 if hour == 12 and meridiem == "am" else hour
    minute = int(minute)

    now = datetime.datetime.now()
    converted = datetime.datetime(year, month, day, hour, minute)

    if now > converted:
        converted = converted.replace(day=day + 1)

    return converted


def get_current_time():
    return datetime.datetime.now()


print(get_time_by_start_stop("start"))
