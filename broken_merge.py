import pandas as pd

left = pd.DataFrame({
    "id": [1, 1, 2],
    "value": [10, 11, 20]
})

right = pd.DataFrame({
    "id": [1, 1, 2],
    "name": ["A", "A_dup", "B"]
})
right = right.drop_duplicates(subset=["id"])

merged = left.merge(right, on="id", how="left")


print(len(left), "->", len(merged))
print(merged)
