# TP02: Working with Big Data Files

## Setup

```bash
python -m pip install -r requirements.txt
```

The repository does not contain a 5GB binary data file. Generate the reproducible test file locally:

```bash
python generate_data.py big.csv --gigabytes 5.1
```

The generator writes a real CSV larger than 5GB with the same four columns used by the benchmark. Delete it after the experiment with `rm big.csv`.

## Benchmark

```bash
python benchmark.py big.csv --method full
python benchmark.py big.csv --method chunks --chunksize 100000
python benchmark.py big.csv --method dask --blocksize 64MB
python benchmark.py big.csv --method all
```

The first command is the traditional OOM test. It uses one `pandas.read_csv` call and is expected to consume substantially more RAM than the other methods. If the operating system kills it, record `Killed` as the result. If Python cannot allocate the dataframe, the script records `MemoryError`.

The chunk method reads exactly 100,000 rows per iteration and maintains only a running sum and count. The Dask method creates one partition per 64MB block. `read_csv` and `mean` create a lazy graph; `compute` executes it with the threaded scheduler. The output includes the number of partitions and graph tasks.

`psutil` samples the current process RSS every 50 milliseconds. Each result is printed as CSV with method, mean, elapsed seconds, peak RSS, and execution details.

## Expected comparison

| Method | Memory behavior | Execution structure |
| --- | --- | --- |
| Pandas full | Highest; may fail on limited RAM | One eager dataframe |
| Pandas chunks | Nearly constant | Sequential 100,000-row batches |
| Dask | Partition-sized working memory | Lazy graph, then parallel partitions |

## Measured 5.1 GiB run

```text
pandas-full,MemoryError,2.09,-,1.5GB memory limit
pandas-chunks,12.40,41.72,185.7,chunksize=100000
dask,12.40,23.76,3811.0,partitions=85 graph_tasks=428
```

## Files

- `generate_data.py`: creates the real 5GB+ CSV locally.
- `benchmark.py`: runs all three required approaches.
- `report.md`: lab report and result table.
- `sample.csv`: small smoke-test fixture.
