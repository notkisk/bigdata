# TP02 Results

The experiment uses `generate_data.py` to create a real 5.1 GiB CSV without storing that large artifact in GitHub.
Standard Pandas reads the whole file eagerly and is the method most likely to exhaust RAM or be killed by the operating system.
Pandas chunking uses 100,000-row batches, so only one batch and two running aggregates remain in memory.
Dask reads 64MB partitions and builds a lazy graph before `compute()` executes it with threads.
The benchmark records elapsed time and peak RSS through `psutil`, while Dask also reports partition and graph-task counts.
The measured run used a 5.10 GiB generated CSV on Linux. The full-read test used a controlled 1.5GB virtual-memory limit so the failure was reproducible without destabilizing the computer.

| Method | Mean temperature | Time | Peak RSS | Details |
| --- | ---: | ---: | ---: | --- |
| Pandas full | MemoryError | 2.09s | - | 1.5GB memory limit |
| Pandas chunks | 12.40 | 41.72s | 185.7MB | chunksize=100000 |
| Dask | 12.40 | 23.76s | 3811.0MB | 85 partitions, 428 graph tasks |
