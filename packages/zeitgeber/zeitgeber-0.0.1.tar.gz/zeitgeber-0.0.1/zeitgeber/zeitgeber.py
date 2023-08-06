import argparse
import datetime

def seconds_since_midnight(datetime_str):
    date, clock = datetime_str.split("_")
    hours, mins, seconds = clock.split("-")
    timestamp = int(hours) * 3600 + int(mins) * 60 + int(seconds)
    return timestamp
