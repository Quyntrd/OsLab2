# project_root/src/ops/sqrt.py
"""
Извлечение квадратного корня: data[out] = sqrt(data[in1])
"""
import math
from file_io import read_all, write_all
from sync_mutex import file_lock

def run(in1: str, out: str) -> None:
    file_lock.acquire()
    data = read_all()
    result = math.sqrt(data[in1])
    data[out] = result
    write_all(data)
    file_lock.release()

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Квадратный корень из значения в файле.')
    parser.add_argument('--in1', required=True)
    parser.add_argument('--out', required=True)
    args = parser.parse_args()
    run(args.in1, args.out)
