import pandas as pd


def parabolic_interpolation(func, interval, pression=1e-5, max_iter=500,
                            flag_results=False, flag_data=False, type_opt='min'):
    """
    Функция поиска экстремума функции методом парабол
    :param func: python function
    :param interval: list consisting of float numbers(left and right bounds)
    :param pression: optimization accuracy
    :param max_iter: maximum amount of iterations
    :param flag_results: output of intermediate results
    :param flag_data: recording intermediate results in a dataset
    :param type_opt: type of extrema: if min:flag_opt=1
                                      if max: flag_opt=-1
    :return: extrema:the point at which the extremum
             df: intermediate results in a dataset
    """

    if type_opt == 'min':
        flag_opt = 1
    else:
        flag_opt = -1

    data = []
    df = pd.DataFrame(columns=['iter', 'point', 'function'])
    x0 = interval[0]
    x1 = interval[1]
    x2 = (x0 + x1) / 2

    f0 = flag_opt * func(x0)
    f1 = flag_opt * func(x1)
    f2 = flag_opt * func(x2)
    f_x = {x0: f0, x1: f1, x2: f2}
    x2, x1, x0 = sorted([x0, x1, x2], key=lambda x: f_x[x])

    if flag_data:
        data = [[0, x2, func(x2)]]
    if flag_results:
        print(f"Номер итерации {0}, точка {x2}, функция {func(x2)} .")


    for i in range(max_iter):

        num = (x1 - x2) ** 2 * (f2 - f0) + (x0 - x2) ** 2 * (f1 - f2)
        den = 2 * ((x1 - x2) * (f2 - f0) + (x0 - x2) * (f1 - f2))
        x_extr = x2 + num / den

        if x_extr == x0 or x_extr == x1 or x_extr == x2:
            print('code 2, точка совпала с уже имеющимися')

        if den == 0:
            print('code 2, невозможно вычислить точку')

        if interval[0] > x_extr > interval[1]:
            print('code 2, точка вышла за интервал')

        f_extr = flag_opt * func(x_extr)

        if f_extr < f2:
            x0, f0 = x1, f1
            x1, f1 = x2, f2
            x2, f2 = x_extr, f_extr

        elif f_extr < f1:
            x0, f0 = x1, f1
            x1, f1 = x_extr, f_extr

        elif f_extr < f0:
            x0, f0 = x_extr, f_extr
        if i == 499:
            print('достигнуто максимальное количество итераций code 1')

        elif abs(x1 - x2) < pression and abs(f1 - f2) < pression:
            print('найдено значение с заданной точностью, code 0')
            break

        if flag_data:
            data.append(([i + 1, x_extr, func(x_extr)]))
            df = pd.DataFrame(data, columns=['iter', 'point', 'function'])

        if flag_results:
            print(f"Номер итерации {i + 1}, точка {x_extr}, функция {func(x_extr)}.")


    return x_extr, df