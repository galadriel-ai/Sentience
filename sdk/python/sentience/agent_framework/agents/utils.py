import datetime


def get_current_timestamp() -> int:
    return int(datetime.datetime.now(datetime.timezone.utc).timestamp())
