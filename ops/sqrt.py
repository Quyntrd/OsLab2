# project_root/src/ops/sqrt.py
import math
from file_io import read_all, write_all
from sync_mutex import file_lock

def run(in1: str, out: str) -> None:
    file_lock.acquire()
    data = read_all()
    if data[in1] < 0:
        file_lock.release()
        raise ValueError(f"Невозможно извлечь корень из отрицательного {in1}={data[in1]}")
    data[out] = math.sqrt(data[in1])
    write_all(data)
    file_lock.release()