# TP02 Results

The full Pandas method loads the complete CSV into memory, so a 5GB file can exhaust RAM before the calculation finishes.
The chunked method reads 100,000 rows at a time and keeps only running sum and count values.
Its memory use stays nearly constant because processed chunks are released before the next chunk is read.
Dask builds a lazy task graph when `read_csv` and `mean` are called.
The graph is executed only by `compute`, allowing partitions to be processed independently.
Chunking is straightforward and predictable, while Dask is better suited to parallel out-of-core work.
