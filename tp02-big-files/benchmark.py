import argparse
import time
from pathlib import Path
from resource import RUSAGE_SELF, getrusage

import dask.dataframe as dd
import pandas as pd


def peak_mb():
    return getrusage(RUSAGE_SELF).ru_maxrss / 1024


def full_read(path):
    started = time.perf_counter()
    frame = pd.read_csv(path)
    result = frame["temperature"].mean()
    return "pandas-full", result, time.perf_counter() - started, peak_mb()


def chunk_read(path, size):
    started = time.perf_counter()
    total = 0.0
    count = 0
    for frame in pd.read_csv(path, chunksize=size):
        values = frame["temperature"].dropna()
        total += values.sum()
        count += values.size
    return "pandas-chunks", total / count, time.perf_counter() - started, peak_mb()


def dask_read(path):
    started = time.perf_counter()
    frame = dd.read_csv(path)
    lazy_mean = frame["temperature"].mean()
    result = lazy_mean.compute()
    return "dask", result, time.perf_counter() - started, peak_mb()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=Path)
    parser.add_argument("--chunksize", type=int, default=100000)
    args = parser.parse_args()
    for method in (full_read, lambda path: chunk_read(path, args.chunksize), dask_read):
        try:
            name, mean, seconds, memory = method(args.file)
            print(f"{name}: mean={mean:.2f} time={seconds:.3f}s peak_rss={memory:.1f}MB")
        except MemoryError:
            print(f"{method.__name__}: MemoryError")


if __name__ == "__main__":
    main()
