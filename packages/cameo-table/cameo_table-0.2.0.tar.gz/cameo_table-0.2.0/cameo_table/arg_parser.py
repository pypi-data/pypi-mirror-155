import pandas as pd
import polars as pl
from .path_handler import *
from .file_handler import *
from .df_handler import *

_supported_types_ = [".parquet", ".csv", ".csv.gz", ".zip",]

def parse_args(path, col_to_apply_on, value, result_path):
    if type(path) is pd.DataFrame() or pl.DataFrame():
        df = pl.DataFrame(path)
    elif not is_url(path) and not file_exists(path):
        raise ValueError(f'{path} does not exist or it is a directory')
    elif ext_str(result_path) not in _supported_types_:
        raise ValueError(f'output file type: {ext_str(result_path)} not supported yet, supported types {_supported_types_}')
    else:
        df = df_readfile(path)
    if df is None:
        raise ValueError(f'input file type: {ext_str(path)} not supported yet, supported types {_supported_types_}')
    pathlib.Path.mkdir(parent(result_path), exist_ok=True, parents=True)
    return df



'''
def int_df_read_csv_gz_from_url(url):
    csv_path = f'{os.getcwd()}/{os.path.split(url)[1]}'
    while(True):
        try:
            content = requests.get(url).content
        except requests.exceptions.RequestException:
            print('\nhttp request error, retry...')
            continue
        break    
    open(csv_path, "wb").write(content)
    try:
        df = pd.read_csv(csv_path, compression='gzip', header=0, sep=',', quotechar='"')
    except:
        #print('[no file found]', end=' ')
        df = None
        os.remove(csv_path)
        return 0,df
    size = os.path.getsize(csv_path)
    os.remove(csv_path)
    return size, df
'''