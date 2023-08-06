import polars as pl
from .file_handler import *

def df_pick_rows_contain_certain_value_on_col(df_in, col_to_apply_on, value):
    df = df_in
    df = df[df[col_to_apply_on]==value]
    return df

def df_turn_vertical_to_horizontal_old(df_in, col_of_label, col_of_value):
    df = df_in
    dup_keys = df.columns
    if col_of_value not in dup_keys or col_of_label not in dup_keys:
        raise ValueError('column index not in dataframe')
    dup_keys.remove(col_of_label)
    dup_keys.remove(col_of_value)
    group_key = dup_keys[0]
    max_count = 0
    for key in dup_keys:
        g = df[dup_keys].groupby(key).n_unique().shape[0]
        if(g>max_count):
            max_count = g
            group_key = key
    indexes = list(df.groupby(col_of_label).groups()[:,0])
    groups = list(df.groupby(group_key).groups()[:,0])
    df_out = pl.DataFrame()
    for group in groups:
        new_row = df[df[group_key]==group][dup_keys][0]
        for index in indexes:
            try:
                tmp = df[df[group_key]==group]
                tmp = tmp[tmp[col_of_label]==index]
                new_row[index] = tmp[col_of_value]
            except Exception as e:
                new_row[index] = [float("NaN")]
        df_out.vstack(new_row, True)
    return df_out

def df_turn_vertical_to_horizontal(df_in, col_of_label, col_of_value):
    # bug: pivot index can not be float
    df_out = df_in
    dup_keys = df_out.columns
    dup_keys.remove(col_of_label)
    dup_keys.remove(col_of_value)
    group_key = dup_keys[0]
    max_count = 0
    for key in dup_keys:
        g = df_out[dup_keys].groupby(key).n_unique().shape[0]
        if(g>max_count):
            max_count = g
            group_key = key
    df_out = df_out.pivot(index = group_key, columns = col_of_label, values = col_of_value)
    df_left = df_in.drop(col_of_label).drop(col_of_value)
    df_left = df_left.distinct(subset=dup_keys)
    df_out = df_out.drop(group_key)
    df_out = df_left.hstack(df_out)
    return df_out

def unit_test_pivot():
    d = {
            "foo":["one", "one", "one", "two", "two", "two"],
            "bar":["A", "B", "C", "A", "B", "C"],
            "baz":[2.0, 2.0, 2.0, 2.0, 2.0, 2.0],
            "value":[11, 12, 13, 14, 15, 16]
        }
    df = pl.DataFrame(d)
    df = df.pivot(index=["foo", "baz"], columns="bar", values="value")
    (df)

if __name__ == '__main__':
    '''
    dfs = df_readfile('test.zip')
    for zipname, df in dfs.items():
        df_turn_vertical_to_horizontal(df, 'sensorId', 'value')
        df_pick_rows_contain_certain_value_on_col(df, 'sensorId', 'temperature')
    '''
    df = df_readfile('deviceId_11094256953_original.csv')
    #print(df.head())
    df = df_turn_vertical_to_horizontal(df, 'sensorId', 'value')
    print(df.head())
    #unit_test_pivot()