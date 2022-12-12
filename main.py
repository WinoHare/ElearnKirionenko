import time

from InputConnect import InputConnect
from Statistics import Statistics

def profiler(func):
    def wrapper(*args, **kwargs):
        before = time.time()
        retval = func(*args, **kwargs)
        after = time.time()
        print(after - before)

    return wrapper

@profiler
def get_report():
    InputConnect()

if __name__ == '__main__':
    print(get_report())

