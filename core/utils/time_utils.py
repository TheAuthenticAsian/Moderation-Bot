from datetime import datetime, timedelta


def convert_time_to_seconds(time):
    time_convert = {"s": 1, "m": 60, "h": 3600, "d": 86400}
    try:
        return int(time[:-1]) * time_convert[time[-1]]
    except:
        return time


def showFutureTime(time):
    now = datetime.now()
    output = convert_time_to_seconds(time)

    add = timedelta(seconds=int(output))
    now_plus_10 = now + add

    return now_plus_10.strftime(r'%m/%d, %H:%M')
