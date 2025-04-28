# project_root/src/main.py
"""
Главный процесс: ввод коэффициентов, инициализация файла, запуск операций и вывод корней.
"""
import multiprocessing
from file_io import read_all, write_all
import ops.multiply as multiply_mod
import ops.subtract as subtract_mod
import ops.add as add_mod
import ops.sqrt as sqrt_mod
import ops.divide as divide_mod

def init_shared(a: float, b: float, c: float) -> None:
    # Базовые коэффициенты и константы
    data = {
        'a': a,
        'b': b,
        'c': c,
        'const4': 4.0,
        'const_neg1': -1.0,
        'const2': 2.0,
    }
    # Инициализация промежуточных полей
    for key in ['b2', 'ac', '4ac', 'D', 'sqrtD', 'neg_b', 'two_a', 'num1', 'num2', 'x1', 'x2']:
        data[key] = 0.0
    write_all(data)


if __name__ == '__main__':
    a = float(input("Введите a: "))
    b = float(input("Введите b: "))
    c = float(input("Введите c: "))

    init_shared(a, b, c)

    # Этап 1: квадраты и простые умножения
    stage1 = [
        multiprocessing.Process(target=multiply_mod.run, args=('b', 'b', 'b2')),
        multiprocessing.Process(target=multiply_mod.run, args=('a', 'c', 'ac')),
        multiprocessing.Process(target=multiply_mod.run, args=('const_neg1', 'b', 'neg_b')),
        multiprocessing.Process(target=multiply_mod.run, args=('const2', 'a', 'two_a')),
    ]
    for p in stage1:
        p.start()
    for p in stage1:
        p.join()

    # Этап 2: 4ac
    p4ac = multiprocessing.Process(target=multiply_mod.run, args=('const4', 'ac', '4ac'))
    p4ac.start(); p4ac.join()

    # Этап 3: дискриминант D = b2 - 4ac
    pD = multiprocessing.Process(target=subtract_mod.run, args=('b2', '4ac', 'D'))
    pD.start(); pD.join()

    # Этап 4: sqrt(D)
    psqrt = multiprocessing.Process(target=sqrt_mod.run, args=('D', 'sqrtD'))
    psqrt.start(); psqrt.join()

    # Этап 5: корни числители
    pnum1 = multiprocessing.Process(target=add_mod.run, args=('neg_b', 'sqrtD', 'num1'))
    pnum2 = multiprocessing.Process(target=subtract_mod.run, args=('neg_b', 'sqrtD', 'num2'))
    pnum1.start(); pnum2.start()
    pnum1.join(); pnum2.join()

    # Этап 6: деление на 2a → x1, x2
    px1 = multiprocessing.Process(target=divide_mod.run, args=('num1', 'two_a', 'x1'))
    px2 = multiprocessing.Process(target=divide_mod.run, args=('num2', 'two_a', 'x2'))
    px1.start(); px2.start()
    px1.join(); px2.join()

    # Вывод результатов
    result = read_all()
    print(f"Корни уравнения: x1 = {result['x1']}, x2 = {result['x2']}")
