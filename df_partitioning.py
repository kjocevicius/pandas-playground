import pandas as pd
import random
import time as t
import utils as u

# This is different from splitting, as order is NOT important!!!
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


def split_df(df, splits_count, remainder):
  return df[df.index % splits_count == remainder]
  

def experiment():
    print('Partitioning indexes directly')
    df = create_dataframe()
    start = t.perf_counter_ns()
    
    remainders = range(0, splits_count)
    partitioned_dfs = map(lambda remainder: split_df(df, splits_count, remainder), remainders)
    partitioned_dfs = list(partitioned_dfs)

    u.duration(start)
    # print(df)

    # for split in partitioned_dfs:
    #   print(split)

experiment()