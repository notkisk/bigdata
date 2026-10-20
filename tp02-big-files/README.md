# TP02: Working with Big Data Files

## Setup

```bash
python -m pip install -r requirements.txt
```

The included `sample.csv` is only a small fixture. For the real experiment, place the 5GB+ CSV beside the script or pass its path directly.

## Run

```bash
python benchmark.py sample.csv
python benchmark.py /path/to/large-file.csv --chunksize 100000
```

The script calculates the mean temperature three ways:

- `pandas-full` uses one `read_csv` call and represents the OOM risk.
- `pandas-chunks` processes 100,000 rows per iteration and keeps a running sum and count.
- `dask` creates a lazy graph, then runs it with `compute()`.

Time is measured with `perf_counter`; peak process RSS is read from Linux resource usage. A full Pandas read can raise `MemoryError` or trigger swapping on the 5GB file, so it should be monitored rather than forced on a low-memory machine.

## Example result

```text
pandas-full: mean=11.93 time=0.010s peak_rss=...MB
pandas-chunks: mean=11.93 time=0.012s peak_rss=...MB
dask: mean=11.93 time=0.180s peak_rss=...MB
```
