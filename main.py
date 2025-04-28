# project_root/src/main.py
"""
Главный процесс: ввод коэффициентов, запуск долгоживущих процессов-операций и распределение задач через очереди.
"""
import os
from multiprocessing import Process, JoinableQueue
from file_io import read_all, write_all
import ops.multiply as multiply_mod
import ops.subtract as subtract_mod
import ops.add as add_mod
import ops.sqrt as sqrt_mod
import ops.divide as divide_mod

# Инициализация shared.txt с исходными данными
def init_shared(a: float, b: float, c: float) -> None:
    data = {'a': a, 'b': b, 'c': c, 'const4': 4.0, 'const_neg1': -1.0, 'const2': 2.0}
    for key in ['b2', 'ac', '4ac', 'D', 'sqrtD', 'neg_b', 'two_a', 'num1', 'num2', 'x1', 'x2']:
        data[key] = 0.0
    write_all(data)

# Воркер для бинарных операций (multiply, subtract, add, divide)
def worker_bin(queue: JoinableQueue, func):
    while True:
        task = queue.get()
        if task is None:
            queue.task_done()
            break
        in1, in2, out = task
        func(in1, in2, out)
        queue.task_done()

# Воркер для унарной операции sqrt
def worker_unary(queue: JoinableQueue, func):
    while True:
        task = queue.get()
        if task is None:
            queue.task_done()
            break
        inp, out = task
        func(inp, out)
        queue.task_done()

if __name__ == '__main__':
    # Ввод коэффициентов
    a = float(input("Введите a: "))
    b = float(input("Введите b: "))
    c = float(input("Введите c: "))

    # Инициализация файла
    init_shared(a, b, c)

    # Создаем очереди для каждого типа операции
    q_mul = JoinableQueue()
    q_sub = JoinableQueue()
    q_add = JoinableQueue()
    q_sqrt = JoinableQueue()
    q_div = JoinableQueue()

    # Стартуем процессы-воркеры
    p_mul = Process(target=worker_bin, args=(q_mul, multiply_mod.run), daemon=True)
    p_sub = Process(target=worker_bin, args=(q_sub, subtract_mod.run), daemon=True)
    p_add = Process(target=worker_bin, args=(q_add, add_mod.run), daemon=True)
    p_sqrt = Process(target=worker_unary, args=(q_sqrt, sqrt_mod.run), daemon=True)
    p_div = Process(target=worker_bin, args=(q_div, divide_mod.run), daemon=True)

    for p in (p_mul, p_sub, p_add, p_sqrt, p_div):
        p.start()

    # Постановка задач
    q_mul.put(('b', 'b', 'b2'))
    q_mul.put(('a', 'c', 'ac'))
    q_mul.put(('const_neg1', 'b', 'neg_b'))
    q_mul.put(('const2', 'a', 'two_a'))
    q_mul.put(('const4', 'ac', '4ac'))
    q_mul.join()

    q_sub.put(('b2', '4ac', 'D'))
    q_sub.join()

    q_sqrt.put(('D', 'sqrtD'))
    q_sqrt.join()

    q_add.put(('neg_b', 'sqrtD', 'num1'))
    q_add.join()
    
    q_sub.put(('neg_b', 'sqrtD', 'num2'))
    q_sub.join()

    q_div.put(('num1', 'two_a', 'x1'))
    q_div.put(('num2', 'two_a', 'x2'))
    q_div.join()

    # Завершение воркеров
    for q in (q_mul, q_sub, q_add, q_sqrt, q_div):
        q.put(None)

    # Ожидание завершения всех
    for p in (p_mul, p_sub, p_add, p_sqrt, p_div):
        p.join()

    # Вывод результатов
    result = read_all()
    print(f"Корни уравнения: x1 = {result['x1']}, x2 = {result['x2']}")
