import numpy as np
import pandas as pd
import utils as u
import json
import time as t

print(__name__)

columns = [ 'portal', 'id', 'some_float', 'some_int']
dtype = np.dtype('<U4,i8,f4,i8')
data = [
  ['fr', 12, 3.14, 90] ,
  ['fr', 14, 3, 100] ,
  ['pl', 15, 3, 100] ,
]
data_as_tuples = [tuple(x) for x in data]

np_arr = np.fromiter(data_as_tuples, dtype=dtype)
df = pd.DataFrame(np_arr)
df.columns = columns
print(df)

start = t.perf_counter_ns()
df_dict = df.to_dict(orient='list')
df_json = json.dumps(df_dict)
u.duration(start, 'orient list')

start = t.perf_counter_ns()
df_json = df.to_json()
u.duration(start, 'orient DEFAULT')

print(df_json)

new_df = pd.read_json(df_json)
print(new_df)