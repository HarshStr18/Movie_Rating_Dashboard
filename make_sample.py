
import pandas as pd
from pathlib import Path

source = Path("dataset/ratings.csv")
destination = Path("dataset/ratings_sample.csv")

first_chunk = True
total_rows = 0

for chunk in pd.read_csv(source, chunksize=500_000):
    sample = chunk.sample(frac=0.01, random_state=42)

    sample.to_csv(
        destination,
        mode="w" if first_chunk else "a",
        header=first_chunk,
        index=False
    )

    total_rows += len(sample)
    first_chunk = False

print("Sample dataset created successfully!")
print("Total sampled rows:", total_rows)
print("Saved at:", destination)
