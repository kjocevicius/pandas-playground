import numpy as np
import pandas as pd
import polars as pl
import utils as u

class CustomLocationIndexer:

  def __init__(self, dataframe):
    self.df = dataframe
  
  def __setitem__(self, keys, value):
    condition_array = keys[0]
    key = keys[1]
    
    result = np.zeros(len(condition_array))
    for idx in range(0, len(condition_array)):
      if condition_array[idx]:
        if isinstance(value, np.ndarray):
          result[idx] = value[idx]
        else:
          result[idx] = value

      self.df[key] = result
    
class CustomDataframe:
  @staticmethod
  def from_dict(data: dict):
    result = CustomDataframe()

    for column_name in data:
      column = data[column_name]
      array = np.array(column)
      result[column_name] = array

    return result

  def __init__(self):
    self.data = dict()
    self.loc = CustomLocationIndexer(self)
    self.size = None

  def __setitem__(self, key, value):    
    if isinstance(value, np.ndarray):
      if self.size is None:
        self.size = len(value)
      elif self.size != len(value):
        raise Exception("Wrong value size")
    else:
      value = np.full(self.size, value)
      
    self.data[key] = value

  def __getitem__(self, key):
    return self.data[key]

some_list = list(range(1, 10000))
some_data = {
  "a": some_list,
  "b": [x + 499 for x in some_list],
  "c": [x * 499 for x in some_list],
  "d": [x - 489 for x in some_list],
  "e": [x / 99 for x in some_list],
}

def benchmark_df(df_from_dict, name):
  print(f'Benchmarking: {name}')
  start_total = u.start()
  
  start = u.start()
  df = df_from_dict(some_data)
  u.duration(start, f'{name} - from_dict')

  start = u.start()
  df["tst_0"] = df["a"] + df["b"] - df["e"]
  u.duration(start, f'{name} - df["tst_0"] = df["a"] + df["b"] - df["e"]')

  start = u.start()
  df["tst_1"] = (df["a"] / df["b"]) - df["e"]
  u.duration(start, f'{name} - df["tst_1"] = (df["a"] / df["b"]) - df["e"]')

  start = u.start()
  df["tst_2"] = df["tst_0"] + df["tst_1"]
  u.duration(start, f'{name} - df["tst_2"] = df["tst_0"] + df["tst_1"]')

  # NOT SUPPORTED BY POLARS
  start = u.start()
  df.loc[df["b"] > 1000, "tst_3"] = 1
  u.duration(start, f'{name} - df.loc[df["b"] > 1000, "tst_3"] = 1')
  
  # NOT SUPPORTED BY POLARS
  start = u.start()
  df.loc[df["b"] > 1000, "tst_4"] = df["tst_0"] + df["tst_1"] + df["tst_2"]
  u.duration(start, f'{name} - df.loc[df["b"] > 1000, "tst_4"] = df["tst_0"] + df["tst_1"] + df["tst_2"]')
  
  u.duration(start_total, f'TOTAL ({name})')


def benchmark_df_polars(df_from_dict, name):
  print(f'Benchmarking: {name}')
  start_total = u.start()
  
  start = u.start()
  df = df_from_dict(some_data)
  u.duration(start, f'{name} - from_dict')

  start = u.start()
  df["tst_0"] = df["a"] + df["b"] - df["e"]
  u.duration(start, f'{name} - df["tst_0"] = df["a"] + df["b"] - df["e"]')

  start = u.start()
  df["tst_1"] = (df["a"] / df["b"]) - df["e"]
  u.duration(start, f'{name} - df["tst_1"] = (df["a"] / df["b"]) - df["e"]')

  start = u.start()
  df["tst_2"] = df["tst_0"] + df["tst_1"]
  u.duration(start, f'{name} - df["tst_2"] = df["tst_0"] + df["tst_1"]')

  # NOT SUPPORTED BY POLARS - TODO : rewrite
  # start = u.start()
  # df.loc[df["b"] > 1000, "tst_3"] = 1
  # u.duration(start, f'{name} - df.loc[df["b"] > 1000, "tst_3"] = 1')
  
  # NOT SUPPORTED BY POLARS - TODO : rewrite
  # start = u.start()
  # df.loc[df["b"] > 1000, "tst_4"] = df["tst_0"] + df["tst_1"] + df["tst_2"]
  # u.duration(start, f'{name} - df.loc[df["b"] > 1000, "tst_4"] = df["tst_0"] + df["tst_1"] + df["tst_2"]')
  
  u.duration(start_total, f'TOTAL ({name})')


# benchmark_df(pd.DataFrame.from_dict, "pd.Dataframe 1") # SLOWER
# benchmark_df(CustomDataframe.from_dict, "CustomDataframe 1") # FASTER
# benchmark_df(pd.DataFrame.from_dict, "pd.Dataframe 2") # FASTER or equal
# benchmark_df(CustomDataframe.from_dict, "CustomDataframe 2") # same -> slower

benchmark_df_polars(pd.DataFrame.from_dict, "pd.Dataframe 1") # SLOWER
benchmark_df_polars(CustomDataframe.from_dict, "CustomDataframe 1") # SLOWER
benchmark_df_polars(pd.DataFrame.from_dict, "pd.Dataframe 2") # SLOWER
benchmark_df_polars(CustomDataframe.from_dict, "CustomDataframe 2") # SLOWER
benchmark_df_polars(pl.DataFrame, "Polars 1") # ??
benchmark_df_polars(pl.DataFrame, "Polars 2") # ??

# Seems like first pd.DataFrame is slower, but after that it gets faster
# CustomDataframe stays with the same performance :(

# Benchmarking: pd.Dataframe
# pd.Dataframe - from_dict: 22.900287
# pd.Dataframe - df["tst_0"] = df["a"] + df["b"] - df["e"]: 1.57747
# pd.Dataframe - df["tst_1"] = (df["a"] / df["b"]) - df["e"]: 0.9156
# pd.Dataframe - df["tst_2"] = df["tst_0"] + df["tst_1"]: 0.7532
# pd.Dataframe - df.loc[df["b"] > 1000, "tst_3"] = 1: 80.065763
# pd.Dataframe - df.loc[df["b"] > 1000, "tst_4"] = df["tst_0"] + df["tst_1"] + df["tst_2"]: 3.72602
# TOTAL (pd.Dataframe): 110.211839

# Benchmarking: CustomDataframe
# CustomDataframe - from_dict: 8.02121
# CustomDataframe - df["tst_0"] = df["a"] + df["b"] - df["e"]: 0.08925
# CustomDataframe - df["tst_1"] = (df["a"] / df["b"]) - df["e"]: 0.05871
# CustomDataframe - df["tst_2"] = df["tst_0"] + df["tst_1"]: 0.04131
# CustomDataframe - df.loc[df["b"] > 1000, "tst_3"] = 1: 66.983214
# CustomDataframe - df.loc[df["b"] > 1000, "tst_4"] = df["tst_0"] + df["tst_1"] + df["tst_2"]: 17.154879
# TOTAL (CustomDataframe): 92.643092

# Benchmarking: pd.Dataframe
# pd.Dataframe - from_dict: 25.233257
# pd.Dataframe - df["tst_0"] = df["a"] + df["b"] - df["e"]: 58.685985
# pd.Dataframe - df["tst_1"] = (df["a"] / df["b"]) - df["e"]: 1.29375
# pd.Dataframe - df["tst_2"] = df["tst_0"] + df["tst_1"]: 0.90365
# pd.Dataframe - df.loc[df["b"] > 1000, "tst_3"] = 1: 1.42668
# pd.Dataframe - df.loc[df["b"] > 1000, "tst_4"] = df["tst_0"] + df["tst_1"] + df["tst_2"]: 2.94332
# TOTAL (pd.Dataframe): 90.777461

# Benchmarking: CustomDataframe
# CustomDataframe - from_dict: 8.113628
# CustomDataframe - df["tst_0"] = df["a"] + df["b"] - df["e"]: 0.149731
# CustomDataframe - df["tst_1"] = (df["a"] / df["b"]) - df["e"]: 0.095871
# CustomDataframe - df["tst_2"] = df["tst_0"] + df["tst_1"]: 0.01392
# CustomDataframe - df.loc[df["b"] > 1000, "tst_3"] = 1: 17.093099
# CustomDataframe - df.loc[df["b"] > 1000, "tst_4"] = df["tst_0"] + df["tst_1"] + df["tst_2"]: 71.580163
# TOTAL (CustomDataframe): 97.39412