import csv
import os
from collections import Counter

path = os.getenv("DATA_FILE", "data/dataset.csv")

with open(path, newline="", encoding="utf-8") as file:
    rows = list(csv.DictReader(file))

scores = [float(row["score"]) for row in rows]
groups = Counter(row["category"] for row in rows)

print(f"Rows: {len(rows)}")
print(f"Average score: {sum(scores) / len(scores):.2f}")
print("Categories:")
for category, count in sorted(groups.items()):
    print(f"  {category}: {count}")
