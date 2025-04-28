# project_root/src/ops/add.py
"""
Сложение: data[out] = data[in1] + data[in2]
"""
from file_io import read_all, write_all
from sync_mutex import file_lock

def run(in1: str, in2: str, out: str) -> None:
    file_lock.acquire()
    data = read_all()
    result = data[in1] + data[in2]
    data[out] = result
    write_all(data)
    file_lock.release()

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Сложение двух значений из файла.')
    parser.add_argument('--in1', required=True)
    parser.add_argument('--in2', required=True)
    parser.add_argument('--out', required=True)
    args = parser.parse_args()
    run(args.in1, args.in2, args.out)
