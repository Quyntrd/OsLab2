# project_root/src/file_io.py
"""
Утилиты для чтения и записи ключ=значение в текстовом файле shared.txt
"""
import os
from typing import Dict

# Путь к файлу с данными (инициализируется в main.py)
SHARED_FILE = os.path.join(os.getcwd(), 'data', 'shared.txt')


def read_all(path: str = SHARED_FILE) -> Dict[str, float]:
    """
    Считывает все строки формата key=value из файла в словарь.
    """
    data: Dict[str, float] = {}
    if not os.path.exists(path):
        return data
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or '=' not in line:
                continue
            key, val = line.split('=', 1)
            data[key.strip()] = float(val.strip())
    return data


def write_all(data: Dict[str, float], path: str = SHARED_FILE) -> None:
    """
    Перезаписывает файл всеми парами key=value (каждая в своей строке).
    """
    directory = os.path.dirname(path)
    os.makedirs(directory, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        for key, val in data.items():
            f.write(f"{key}={val}\n")
