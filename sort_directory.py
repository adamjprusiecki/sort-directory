import argparse
import sys
import os
from pathlib import Path
import shutil

def parse_args(argv: list):
    parser = argparse.ArgumentParser(
        prog='sort_directory.py',
        description='Sorts a nested directory by keyword/key phrase',
        formatter_class=argparse.RawTextHelpFormatter,
    )

    parser.add_argument(
        '--input',
        '-i',
        help='Path of nested/unorganized directory',
        nargs='?',
        required=False,
        default='test_input'
    )

    parser.add_argument(
        '--output',
        '-o',
        help='Path of the directory for the sorted output directory',
        nargs='?',
        required=False,
        default='test_output'
    )

    parser.add_argument(
        '--key',
        '-k',
        help='Key to sort/organize by',
        nargs='?',
        required=False,
        default='.csv,.txt'
    )

    args = parser.parse_args(argv)
    return args

def sort_dir(input_dir: Path, output_dir: Path, key_list: list, sub_dir=None):
    if sub_dir == None:
        directory = input_dir
    else:
        directory = sub_dir

    dir_list = os.listdir(directory)
    for file_str in dir_list:
        is_match = False
        if Path(directory.joinpath(file_str)).is_file(): # If is file
            for key_str in key_list:
                    if key_str in file_str:
                        shutil.copy(directory.joinpath(file_str), output_dir.joinpath(key_str,file_str))
                        is_match = True
        else: # If is dir
            sort_dir(input_dir=input_dir,output_dir=output_dir,key_list=key_list,sub_dir=Path(directory.joinpath(file_str)))
        if is_match == False:
            if Path(directory.joinpath(file_str)).is_file(): 
                shutil.copy(directory.joinpath(file_str), output_dir.joinpath('misc'))

def create_directories(input_dir: Path, output_dir: Path, key_list: list):
    if not os.path.exists(input_dir):
        raise FileNotFoundError('The path you have entered does not exist')
    else:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        else:
            shutil.rmtree(output_dir)
            os.makedirs(output_dir)
    
    for key_str in key_list:
        if not os.path.exists(output_dir.joinpath(key_str)):
            os.makedirs(output_dir.joinpath(key_str))
    if not os.path.exists(output_dir.joinpath('misc')):
        os.makedirs(output_dir.joinpath('misc'))

if __name__ == '__main__':
    args = parse_args(sys.argv[1:])

    input_dir = Path(args.__dict__['input'])
    output_dir = Path(args.__dict__['output'])
    key_list = args.__dict__['key'].split(',')

    create_directories(input_dir, output_dir, key_list)
    sort_dir(input_dir,output_dir,key_list)
