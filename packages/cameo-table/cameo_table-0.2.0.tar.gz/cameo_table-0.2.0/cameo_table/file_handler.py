import polars as pl
import pandas as pd
from .path_handler import *
import zipfile
import zlib
import gzip
import requests
import os

def name_df_dict_read_zip(path):
    d = dict()
    zip_info_list = zipfile.ZipFile(path).infolist()
    for f in zip_info_list:
        df = df_readfile(f.filename, zipfile.ZipFile(path).read(name=f))
        if df:
            d[f.filename] = df
    return d

def df_readfile(path, f=None):
    if not f:
        f = path
    if is_url(path):
        dl_file_path = f'tmp/{pathlib.Path(path).name}'
        pathlib.Path('tmp').mkdir(parents=True, exist_ok=True)
        content = requests.get(path).content
        open(dl_file_path, "wb").write(content)
        df_out  = df_readfile(dl_file_path)
        os.remove(dl_file_path)
        return df_out
    elif is_csv(path):
        return pl.read_csv(f)
    elif is_csv_gz(path):
        return pl.read_csv(f, gzip=True)
    elif is_parquet(path):
        return pl.read_parquet(f)
    elif is_zip(path):
        return name_df_dict_read_zip(path)
    else:
        raise ValueError(f'Invalid file format: {ext_str(f)}')

def output_file_from_df(df, path):
    if is_csv(path):
        df.to_csv(path)
    elif is_csv_gz(path):
        df.to_csv(path, gzip=True)
    elif is_parquet(path):
        df.to_parquet(path)
    else:
        raise ValueError(f'Invalid file format: {ext_str(path)}')

def output_str_from_df(df, path):
    if is_csv(path):
        return df.to_csv()
    elif is_csv_gz(path):
        s = df.to_csv()
        b = bytes(f'\ufeff{s}', 'utf-8')
        return gzip.compress(b)
    
    elif is_parquet(path):
        return df.to_parquet()
        pl.DataFrame().to_csv()
    else:
        raise ValueError(f'Invalid file format: {ext_str(path)}')

if __name__ == "__main__":
    path = 'test.csv.gz'
    d = df_readfile(path)
    if not is_zip(path):
        #print(d.head())
        print(d.to_csv())
    else:
        for name, df in d.items():
            print(name, df.head())