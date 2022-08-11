import pandas as pd
import numpy as np
import random
import time as t
import utils as u

# This is different from partitoning, as order is important!!!
print(__name__)

columns_map = {
    'number': 'numeris',
    'numberPlusOne': 'numerisPliusVienas',
    'numberPlusOneHundred': 'numerisPliusSimtas',
    'numberAsString': 'numerisStringas'
}
columns = columns_map.keys()
new_columns_names = columns_map.values()
rows_count = 9733

random_numbers = random.sample(range(1, 100000), rows_count)
data = list(
    map(lambda number: [number, number + 1, number + 100,
                        str(number)], random_numbers))

splits_count = 4


def create_dataframe():
    return pd.DataFrame(data, columns=columns)

  
def split_df(df, splits_count):
  return np.array_split(df, splits_count)
  

def experiment():
    df = create_dataframe()
    print(f"Split df of len {len(df.index)} to {splits_count} parts")
    # print(df)
  
    start = t.perf_counter_ns()
    partitioned_dfs = split_df(df, splits_count)
    u.duration(start)

    for split in partitioned_dfs:
      print(split)

experiment()