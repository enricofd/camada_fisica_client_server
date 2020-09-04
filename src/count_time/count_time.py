import time


def time_to_bytes():

    main = str(time.time()).split(".")[0]
    mili_raw = str(time.time()).split(".")[1]
    mili = mili_raw if len(mili_raw) == 7 else mili_raw + "0"

    first = [int(x) for x in main]
    second = [int(x) for x in mili]


    return bytes(first + second)
