import argparse
import threading
import time
from pathlib import Path

import dask.dataframe as dd
import pandas as pd
import psutil


class MemoryWatch:
    def __init__(self):
        self.process = psutil.Process()
        self.highest = 0
        self.running = True
        self.thread = threading.Thread(target=self.watch, daemon=True)

    def watch(self):
        while self.running:
            self.highest = max(self.highest, self.process.memory_info().rss)
            time.sleep(0.05)

    def __enter__(self):
        self.thread.start()
        return self

    def __exit__(self, *_):
        self.running = False
        self.thread.join()


def measure(name, action):
    started = time.perf_counter()
    try:
        with MemoryWatch() as memory:
            value, detail = action()
        print(f"{name},{value:.2f},{time.perf_counter() - started:.2f},{memory.highest / 1024 ** 2:.1f},{detail}")
    except MemoryError:
        print(f"{name},MemoryError,{time.perf_counter() - started:.2f},-,allocation failed")


def full(path):
    def action():
        frame = pd.read_csv(path)
        return frame["temperature"].mean(), "single dataframe"
    measure("pandas-full", action)


def chunks(path, size):
    def action():
        total = 0.0
        count = 0
        for frame in pd.read_csv(path, chunksize=size):
            values = frame["temperature"].dropna()
            total += values.sum()
            count += values.size
        return total / count, f"chunksize={size}"
    measure("pandas-chunks", action)


def dask(path, blocksize):
    def action():
        frame = dd.read_csv(path, blocksize=blocksize, dtype={"temperature": "float64"})
        lazy = frame["temperature"].mean()
        detail = f"partitions={frame.npartitions} graph_tasks={len(lazy.dask)}"
        return lazy.compute(scheduler="threads"), detail
    measure("dask", action)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=Path)
    parser.add_argument("--method", choices=("all", "full", "chunks", "dask"), default="all")
    parser.add_argument("--chunksize", type=int, default=100000)
    parser.add_argument("--blocksize", default="64MB")
    args = parser.parse_args()
    print("method,mean,time_seconds,peak_rss_mb,details")
    if args.method in ("all", "full"):
        full(args.file)
    if args.method in ("all", "chunks"):
        chunks(args.file, args.chunksize)
    if args.method in ("all", "dask"):
        dask(args.file, args.blocksize)


if __name__ == "__main__":
    main()
