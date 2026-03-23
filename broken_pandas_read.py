import pandas as pd
from io import StringIO

csv_text = "id;value\n1;10\n2;20\n3;30\n"
csv_text_2 = "id;value\n1;10\n\n3;30\n"
csv_text_3 = "id;value\n1;10\n2;\n3;30\n"

# BUG: sep не указан -> pandas ожидает запятую
df = pd.read_csv(StringIO(csv_text), sep=";")

print(df.head())
print(df.dtypes)
print(df["value"].mean())
