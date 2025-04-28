# project_root/src/ops/divide.py
from file_io import read_all, write_all
from sync_mutex import file_lock

def run(in1: str, in2: str, out: str) -> None:
    file_lock.acquire()
    data = read_all()
    if data[in2] == 0:
        file_lock.release()
        raise ZeroDivisionError(f"Деление на ноль: {in2}={data[in2]}")
    data[out] = data[in1] / data[in2]
    write_all(data)
    file_lock.release()