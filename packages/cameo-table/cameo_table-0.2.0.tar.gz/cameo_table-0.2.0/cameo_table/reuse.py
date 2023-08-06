import datetime as dt
import psutil
import os

def float_memory_usage():
    return round(psutil.Process(os.getpid()).memory_info().rss/1000000,2)

def dt_sec_timer():
    '''usage:
    timer = dt_sec_timer()
    'next(timer)' will return/yield the time since last call of 'next(timer)'
    if it's first to be called, it will return/yield 0.00
    '''
    start_time = dt.datetime.now()
    while True:
        end_time = dt.datetime.now()
        last_exec = (end_time - start_time).total_seconds()
        start_time = dt.datetime.now()
        yield last_exec

def df_drop_columns_except(df, exception):
    df_out = df.loc[:, df.columns.isin(exception)]
    return df_out
    
def sec_to_HMS(sec):
    return '{H:0>2d}:{M:0>2d}:{S:0>2d}'.format(H=int(int(sec)/3600), M=int(int(sec)%3600/60), S=int(sec)%60)
    
def list_listfile(mypath):
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    return onlyfiles

