import pandas as pd
import random
import time as t
import utils as u

print(__name__)

columns_map = {
    'number': 'numeris',
    'numberPlusOne': 'numerisPliusVienas',
    'numberPlusOneHundred': 'numerisPliusSimtas',
    'numberAsString': 'numerisStringas'
}
columns = columns_map.keys()
new_columns_names = columns_map.values()

random_numbers = random.sample(range(1, 100000), 10000)
data = list(
    map(lambda number: [number, number + 1, number + 100,
                        str(number)], random_numbers))


def create_dataframe():
    return pd.DataFrame(data, columns=columns)


def usingRename():
    df = create_dataframe()
    start = t.perf_counter_ns()
    df = df.rename(columns_map)
  
    u.duration(start, 'Rename using `.rename`')
    # print(df)


def usingRenameInplace():
    df = create_dataframe()
    start = t.perf_counter_ns()
    df.rename(columns_map, inplace=True)
  
    u.duration(start, 'Rename using `.rename` + inplace: true')
    # print(df)


def usingColumnNamesReplace1():
    df = create_dataframe()
    start = t.perf_counter_ns()
    df.columns = new_columns_names
  
    u.duration(start, 'Rename using `.rename` + inplace: true')
    # print(df)


def usingColumnNamesReplace2():
    df = create_dataframe()
    start = t.perf_counter_ns()

    columns_to_replace = columns_map.keys()
    new_columns = []
    for col in df.columns:
        if col in columns_to_replace:
            col = columns_map[col]
        new_columns.append(col)
    df.columns = new_columns

    u.duration(start, 'Rename by changing columns')
    # print(df)


usingRename()
usingRenameInplace()
usingColumnNamesReplace1()
usingColumnNamesReplace2()
