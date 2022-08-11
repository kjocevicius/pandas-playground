import numpy as np
import pandas as pd

print(__name__)

columns = ['portal', 'id', 'some_float', 'some_int']
dtype = np.dtype('<U4,i8,f4,i8')
data = [
    ['fr', 12, 3.14, 90],
    ['fr', 14, 3, 100],
    ['pl', 15, 3, 100],
    [None, 15, 3, 100],
]
data_as_tuples = [tuple(x) for x in data]

np_arr = np.fromiter(data_as_tuples, dtype=dtype)
df = pd.DataFrame(np_arr)
df.columns = columns
print(df)

type = type(df['portal'][3])
print(f'Type of df["portal"][3] is {type}')