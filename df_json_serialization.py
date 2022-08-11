import numpy as np
import pandas as pd

print(__name__)

columns = ['portal', 'id', 'some_float', 'some_int']
dtype = np.dtype('<U4,i8,f4,i8')
data = [
    ['fr', 12, 3.14, 90],
    ['fr', 14, 3, 100],
    ['pl', 15, 3, 100],
]
data_as_tuples = [tuple(x) for x in data]

np_arr = np.fromiter(data_as_tuples, dtype=dtype)
df = pd.DataFrame(np_arr)
df.columns = columns
print(df)

df_json = df.to_json()
# df_json = json.dumps(df) # This won't work
print(df_json)

new_df = pd.read_json(df_json)
print(new_df)
