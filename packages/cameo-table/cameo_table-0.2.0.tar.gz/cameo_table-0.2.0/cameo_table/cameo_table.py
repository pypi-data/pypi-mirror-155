import polars as pl
import pandas as pd
from .path_handler import *
from .file_handler import *
from .df_handler import *
from .arg_parser import *

def pick_rows_contain_certain_value(path, col_to_apply_on, value, result_path="result.parquet"):
    df = parse_args(path, col_to_apply_on, value, result_path)

    if is_single_file(path):
        df = df_pick_rows_contain_certain_value_on_col(df, col_to_apply_on, value)
        output_file_from_df(df, result_path)
    else:
        with zipfile.ZipFile(result_path,'a') as output_file:
            for name,d in df.items():
                d = df_pick_rows_contain_certain_value_on_col(d, col_to_apply_on, value)
                output_file.writestr(name, output_str_from_df(d, name))

def turn_vertical_to_horizontal(path, col_to_apply_on, value, result_path="result.parquet"):
    df = parse_args(path, col_to_apply_on, value, result_path)

    if is_single_file(path):
        df = df_turn_vertical_to_horizontal(df, col_to_apply_on, value)
        output_file_from_df(df, result_path)
    else:
        with zipfile.ZipFile(result_path,'a') as output_file:
            for name,d in df.items():
                d = df_turn_vertical_to_horizontal(d, col_to_apply_on, value)
                output_file.writestr(name, output_str_from_df(d, name))

if __name__ == '__main__':
    n = input('選擇想要的功能 輸入1:挑選出指定欄位為某值的所有列 輸入2:將直欄轉換為橫向資料 輸入0:離開\n')
    while(n!='0'):
        if(n=='1'):
            print('已選功能1:挑選出指定欄位為某值的所有列')
            path, col_to_apply_on, value, result_path = input('以空白隔開 請依序輸入:要處理的檔名(路徑/url) 指定值所在的欄位 指定的值 輸出的檔名(路徑)\n').split(' ')
            pick_rows_contain_certain_value(path = path, col_to_apply_on = col_to_apply_on, value = value, result_path = result_path)
        elif(n=='2'):
            print('已選功能2:將直欄轉換為橫向資料')
            path, col_to_apply_on, value, result_path = input('以空白隔開 請依序輸入:要處理的檔名(路徑/url) 轉換為欄位標題的欄位 對應值所在的欄位 輸出的檔名(路徑)\n').split(' ')
            turn_vertical_to_horizontal(path = path, col_to_apply_on = col_to_apply_on, value = value, result_path = result_path)
        n = input('選擇想要的功能 輸入1:挑選出指定欄位為某值的所有列 輸入2:將直欄轉換為橫向資料 輸入0:離開\n')