import argparse
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    parser.add_argument("--gigabytes", type=float, default=5.1)
    args = parser.parse_args()
    row = b"2026-01-01T00:00:00,A01,12.4,18\n"
    target = int(args.gigabytes * 1024 ** 3)
    block = row * 10000
    written = 0
    with args.output.open("wb") as file:
        file.write(b"timestamp,station,temperature,wind_kmh\n")
        written += 39
        while written < target:
            chunk = block[: min(len(block), target - written)]
            file.write(chunk)
            written += len(chunk)
    print(f"created {args.output} ({written / 1024 ** 3:.2f} GiB)")


if __name__ == "__main__":
    main()
