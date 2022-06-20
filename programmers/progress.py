import time

_current = 1
_total = 1

start = None

def progress_start(total):
    global _current, _total, start
    _current = 1
    _total = total
    start = time.time()

def print_time(seconds):
    if type(seconds) == float:
        seconds = int(seconds)
    
    hours = 0
    minutes = 0

    if seconds > 60:
        minutes = seconds // 60
        seconds %= 60
    if minutes > 60:
        hours = minutes // 60
        minutes %= 60
    
    timestr = "{:0>2}".format(str(seconds))
    if minutes:
        timestr = "{:0>2}".format(str(minutes)) + ":" + timestr
    if hours:
        timestr = str(hours) + ":" + timestr
    
    return timestr


def progress(current: int = -1):
    global _current
    if current < 0:
        _current += 1
    elif current == 0:
        pass
    else:
        _current = current

    elapsed = time.time() - start
    remain = elapsed * (_total - _current) / _current
    tot_time = elapsed * _total / _current

    print(f"{_current}/{_total} ({print_time(remain)}/{print_time(tot_time)})", end="\r")