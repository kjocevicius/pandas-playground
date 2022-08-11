import numpy as np
import pandas as pd

print(__name__)

def print_dtypes(df, columns):
  print(list(map(lambda c: df[c].dtype, columns)))

columns = [ 'portal', 'id', 'some_float', 'some_int']
dtype = np.dtype('<U4,i8,f4,i8')
data = [
  ['fr', 12, 3.14, 90] ,
  ['fr', 14, 3, 100] ,
  ['fr', 15, 3, 100] ,
]
data_as_tuples = [tuple(x) for x in data]

print('----- array')
np_arr = np.array(data_as_tuples, dtype=dtype)
print(np_arr)
df = pd.DataFrame(np_arr)
df.columns = columns
print_dtypes(df, columns)
print(df)

print('----- fromiter')
np_arr = np.fromiter(data_as_tuples, dtype=dtype)
df = pd.DataFrame(np_arr)
df.columns = columns
print_dtypes(df, columns)
print(df)

print('----- array, no dtype')
np_arr = np.array(data)
df = pd.DataFrame(np_arr, columns=columns)
print_dtypes(df, columns)
print(df)

print('=====')