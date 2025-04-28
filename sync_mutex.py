# project_root/src/sync_mutex.py
"""
Единственный мьютекс для защиты операций над shared.txt
"""
from multiprocessing import Lock

file_lock = Lock()
