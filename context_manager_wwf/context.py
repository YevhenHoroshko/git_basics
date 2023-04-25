import time
import sys


class Benchmark:

    def __init__(self, timer=time.perf_counter, stream=sys.stdout, islog=True):
        self.timer = timer
        self.stream = stream
        self.islog = islog

    def __enter__(self):
        """This is called before entering context manager block."""
        self.tstart = self.timer()  # save time when we started

        if self.islog:
            print(f'Entering block @ {self.tstart}', file=self.stream)

        # returned value is assigned to with clause
        # e.g. with .... as val:
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """This is called before returning from context manager block."""
        curtime = self.timer()

        if self.islog:
            print(f'Exiting block @ {curtime}', file=self.stream)

        took = curtime - self.tstart  # compute time delta

        msg = ''
        if exc_type is not None:  # not None means there were an exc raised
            msg += '[INTERRUPTED] '

        msg += f'Took {took * 1000:.3f} ms'
        print(msg, file=self.stream)

        # return True


if __name__ == '__main__':
    # Measure some language statements
    with Benchmark(islog=True) as bench:
        l = list(range(1000))
        max(l)
        # get something from bench obj
        cur = bench.timer()
        sum(l)

    # (almost) the same as
    bench = Benchmark(islog=True)
    with bench:
        l = list(range(1000))
        max(l)
        # get something from bench obj
        cur = bench.timer()
        sum(l)

    import random

    # Measure time of generating 1 MiB
    # of random bytes in 1 KiB chunks
    with Benchmark(islog=False):
        for i in range(1024):
            bt = random.randbytes(1024)
