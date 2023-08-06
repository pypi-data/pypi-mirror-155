import pathlib
import zipfile

def parent(path):
    return pathlib.Path(path).parent

def file_exists(path):
    return pathlib.Path(path).exists() and not pathlib.Path(path).is_dir()

def ext_parser(path):
    return pathlib.Path(path).suffixes

def ext_str(path):
    filetypelist = ext_parser(path)
    filetype = ''
    for ext in filetypelist:
        filetype += f'{ext}'
    return filetype

def is_url(path):
    return path[0:7].lower()=='http://' or path[0:8].lower()=='https://'

def is_zip(path):
    if type(path) is zipfile.ZipInfo:
        path = path.filename
    file_ext = ext_parser(path)
    return file_ext[-1] == '.zip'

def is_csv(path):
    if type(path) is zipfile.ZipInfo:
        path = path.filename
    file_ext = ext_parser(path)
    return file_ext[-1] == '.csv'

def is_parquet(path):
    if type(path) is zipfile.ZipInfo:
        path = path.filename
    file_ext = ext_parser(path)
    return file_ext[-1] == '.parquet'

def is_csv_gz(path):
    if type(path) is zipfile.ZipInfo:
        path = path.filename
    file_ext = ext_parser(path)
    return file_ext[-2:] == ['.csv', '.gz']

def is_single_file(path):
    return not is_zip(path)

def filename_without_ext(path):
    path_out = path
    while(pathlib.Path(path_out).suffixes):
        path_out = pathlib.Path(path_out).stem
    return path_out

if __name__ == '__main__':
    print(ext_str('path/to/file/abc.def.ghi.jkl'))
    print(ext_parser('HtTp://abc.def.ghi.jkl'))