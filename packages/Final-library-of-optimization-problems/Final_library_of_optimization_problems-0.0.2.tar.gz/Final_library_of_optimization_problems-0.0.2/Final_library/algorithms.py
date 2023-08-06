#!/usr/bin/env python
# coding: utf-8

# In[2]:


from Final_library import utils
import sympy as sp
import sympy
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
import pandas as pd
import random
import warnings
import time
import scipy.optimize
from sympy.utilities.lambdify import implemented_function
from IPython.display import display, HTML
from scipy.optimize import line_search, fmin, linprog
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import make_classification, make_blobs
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, mean_squared_error, r2_score,mean_absolute_error
from sklearn.preprocessing import PolynomialFeatures
import re
from tqdm.notebook import tqdm
warnings.filterwarnings('ignore')


# In[2]:


def extremas_searching():
    """
    Запрашивает у пользователя входную функцию, её аргументы, ограничения (если есть) и ограничивающую функцию
    Находит методом Лагранжа точки экстремумов функции, строит на графике исходную и ограничивающую функцию и отображает на найденные точки
        Возвращаемое значение:
                    stationary_points (list): Список, состоящий из найденных точек экстремумов
    """
    is_restricted = 1 if input('Есть ли ограничивающая функция: 1-да/0-нет: ')=='1' else 0
    _input = utils._take_input_extremas_searching(is_restricted)
    varnames = _input['varnames']
    assert isinstance(varnames, list), 'список переменных задан неверно'
    args = sympy.symbols(varnames)
    func = _input['func']
    assert isinstance(func, str), 'функция задана неверно'
    func = sympy.sympify(func)
    bounds = _input['bounds']
    if is_restricted:
        restriction = _input['restriction']
        assert isinstance(restriction, str), 'ограничивающая функция задана неверно'
        restriction = sympy.sympify(restriction)
        lambda_ = sympy.Symbol('lambda')
        lagrangian = func + lambda_*restriction
        partial_first = [lagrangian.diff(arg) for arg in args+[lambda_]]
        stationary_points = sympy.solve(partial_first, args+[lambda_], dict=True)
    else:
        partial_first = [func.diff(arg) for arg in args]
        stationary_points = sympy.solve(partial_first, args, dict=True)

    stationary_points = utils._make_real(stationary_points, args)
    
    hesse = utils._get_hessian(func, args)
    for point in stationary_points:
        for arg in args:
            point[arg] = float(point[arg])
            point['F'] = float(func.subs(point))
            point['type'] = utils._check_point(hesse, point)
                
    if bounds:
        assert isinstance(bounds, dict), 'ограничения заданы неверно'
        stationary_points = utils._filter_points(args, stationary_points, bounds)
        
    if not stationary_points:
        print('Нет стационарных точек')
    
    if is_restricted:
        utils._plot(func, stationary_points, restriction=restriction, bounds=bounds)
    else:
        utils._plot(func, stationary_points, bounds=bounds)
    return stationary_points




def golden_ratio(func, bounds, accuracy=10e-5, max_iter=500, show_interim_results=False, show_convergency=False, return_data=False):
    '''
    Находит минимум функции методом золотого сечения на заданном интервале.
            Параметры:
                    func (function): 
                        Исследуемая функция
                    bounds (tuple or list):
                        Исследуемый интервал
                    accuracy (float, default=None):
                        Точность метода
                    max_iter (int, default=None):
                        Максимальное количество итераций
                    show_interim_results (bool, default=False):
                        Если True, выводит на экран датасет с промежуточными результатами
                    show_convergency (bool, default=False):
                        Если True, выводит на экран график сходимости алгоритма
                    return_data (bool, default=False):
                        Если True, добавляет в возвращаяемый словарь датасет с промежуточными результатами
                        
            Возвращаемое значение:
                    result (dict):
                        Словарь, значениями которого являются точка минимума функции, значение функции в этой точке и флаг
                    
    '''
    iter_num = 0
    left, right = bounds
    ratio = (np.sqrt(5) - 1) / 2    
    interim_results = pd.DataFrame(columns=['N', 'a', 'b', 'x', 'y', 'f(x)', 'f(y)'])
    
    while abs(right - left) > accuracy:
        if iter_num >= max_iter:
            break
            
        x = right - ratio*(right - left)
        y = left + ratio*(right - left)
        
        row = {
            'N': iter_num,
            'a': left,
            'b': right,
            'x': x,
            'y': y,
            'f(x)': func(x),
            'f(y)': func(y)
        }
        interim_results = interim_results.append(row, ignore_index=True)

        if func(x) < func(y):
            right = y
        else:
            left = x
        
        iter_num += 1
    
    flag = 1 if iter_num >= max_iter else 0
    x_min = (left + right) / 2
    f_min = func(x_min)
    
    interim_results.set_index('N', inplace=True)
    if show_interim_results:
        display(HTML(interim_results.to_html()))
    if show_convergency:
        interval_sizes = list(interim_results['b'] - interim_results['a'])
        utils._show_convergency(interval_sizes)
    result = {'arg': x_min, 'func': f_min, 'flag': flag}
    if return_data:
        result['data'] = interim_results
    return result


# In[5]:


def parabola_method(func, bounds, accuracy=10e-5, max_iter=500, show_interim_results=False, show_convergency=False, return_data=False):
    '''
    Находит минимум функции парабол на заданном интервале.
            Параметры:
                    func (function): 
                        Исследуемая функция
                    bounds (tuple or list):
                        Исследуемый интервал
                    accuracy (float, default=None):
                        Точность метода
                    max_iter (int, default=None):
                        Максимальное количество итераций
                    show_interim_results (bool, default=False):
                        Если True, выводит на экран датасет с промежуточными результатами
                    show_convergency (bool, default=False):
                        Если True, выводит на экран график сходимости алгоритма
                    return_data (bool, default=False):
                        Если True, добавляет в возвращаяемый словарь датасет с промежуточными результатами
                        
            Возвращаемое значение:
                    result (dict):
                        Словарь, значениями которого являются точка минимума функции, значение функции в этой точке и флаг
                    
    '''
    iter_num = 0
    left, right = bounds
    x1, x2, x3 = left, (left + right) / 2, right
    prev_min = (left + right) / 2
    curr_min = utils._find_center(func, x1, x2, x3)
    interim_results = pd.DataFrame(columns=['N', 'x1', 'x2', 'x3', 'u', 'f(u)'])
    
    while abs(curr_min - prev_min) > accuracy:
        if iter_num >= max_iter:
            break
            
        c = min(x2, curr_min)
        d = max(x2, curr_min)
        
        row = {
            'N': iter_num,
            'x1': x1,
            'x2': x2,
            'x3': x3,
            'u': curr_min,
            'f(u)': func(curr_min)
        }
        interim_results = interim_results.append(row, ignore_index=True)
        
        if func(c) < func(d):
            x1, x2, x3 = x1, c, d
        else:
            x1, x2, x3 = c, d, right
            
        prev_min = curr_min
        curr_min = utils._find_center(func, x1, x2, x3)
            
        iter_num += 1

    flag = 1 if iter_num >= max_iter else 0
    interim_results.set_index('N', inplace=True)
    if show_interim_results:
        display(HTML(interim_results.to_html()))
    if show_convergency:
        interval_sizes = list(interim_results['x3'] - interim_results['x1'])
        utils._show_convergency(interval_sizes)
    result = {'arg': curr_min, 'func': func(curr_min), 'flag': flag}
    if return_data:
        result['data'] = interim_results
    return result


# In[6]:


def combined_brent(func, bounds, accuracy=10e-5, max_iter=500, show_interim_results=False, show_convergency=False, return_data=False):
    '''
    Находит минимум функции комбинированным методом Брента на заданном интервале.
            Параметры:
                    func (function): 
                        Исследуемая функция
                    bounds (tuple or list):
                        Исследуемый интервал
                    accuracy (float, default=None):
                        Точность метода
                    max_iter (int, default=None):
                        Максимальное количество итераций
                    show_interim_results (bool, default=False):
                        Если True, выводит на экран датасет с промежуточными результатами
                    show_convergency (bool, default=False):
                        Если True, выводит на экран график сходимости алгоритма
                    return_data (bool, default=False):
                        Если True, добавляет в возвращаяемый словарь датасет с промежуточными результатами
                        
            Возвращаемое значение:
                    result (dict):
                        Словарь, значениями которого являются точка минимума функции, значение функции в этой точке и флаг
                    
    '''
    iter_num = 0
    ratio = (3 - np.sqrt(5)) / 2
    
    left, right = bounds
    x_min = w = v = left + ratio*(right - left)
    d_curr = d_prev = right - left
    
    interim_results = pd.DataFrame(columns=['a', 'b', 'x', 'w', 'v', 'u'])
    
    while max(x_min - left, right - x_min) > accuracy:
        if iter_num >= max_iter:
            break
            
        g = d_prev / 2
        d_prev = d_curr
        u = utils._find_center(func, x_min, w, v)
        if not u or (u < left or u > right) or abs(u - x_min) > g:
            if x_min < (left + right) / 2:
                u = x_min + ratio*(right - x_min)
                d_prev = right - x_min
            else:
                u = x_min - ratio*(x_min - left)
                d_prev = (x_min - left)
        d_curr = abs(u - x_min)
        
        row = {
            'N': iter_num,
            'a': left,
            'b': right,
            'x': x_min,
            'w': w,
            'v': v,
            'u': u
        }
        interim_results = interim_results.append(row, ignore_index=True)
        
        if func(u) > func(x_min):
            if u < x_min:
                left = u
            else:
                right = u
            if func(u) <= func(w) or w == x_min:
                v = w
                w = u
            else:
                if func(u) <= func(v) or v == x_min or v == w:
                    v = u
        else:
            if u < x_min:
                right = x_min
            else:
                left = x_min
            v = w
            w = x_min
            x_min = u
            
        iter_num += 1
        
    flag = 1 if iter_num >= max_iter else 0
    interim_results.set_index('N', inplace=True)
    if show_interim_results:
        display(HTML(interim_results.to_html()))
    if show_convergency:
        interval_sizes = list(interim_results['b'] - interim_results['a'])
        utils._show_convergency(interval_sizes)
    result = {'arg': x_min, 'func': func(x_min), 'flag': flag}
    if return_data:
        result['data'] = interim_results
    return result


# In[7]:


def bfgs_method(func, x0, c1=10e-4, c2=0.1, max_iter=500, max_arg=100, accuracy=10e-5, show_interim_results=False, return_data=False):
    '''
    Находит минимум функции методом BFGS.
            Параметры:
                    func (function): 
                        Исследуемая функция
                    x0 (float):
                        Начальная точка
                    c1 (float, default=None):
                        Первый параметр условия Вольфе
                    c2 (float, default=None):
                        Второй параметр условия Вольфе
                    max_iter (int, default=None):
                        Максимальное количество итераций
                    max_arg (float, default=None):
                        Ограничение на максимальное значение аргумента
                    accuracy (float, default=None):
                        Точность метода
                    show_interim_results (bool, default=False):
                        Если True, выводит на экран датасет с промежуточными результатами
                    return_data (bool, default=False):
                        Если True, добавляет в возвращаяемый словарь датасет с промежуточными результатами
                        
            Возвращаемое значение:
                    result (dict):
                        Словарь, значениями которого являются точка минимума функции, значение функции в этой точке и флаг
                    
    '''
    func = sp.sympify(func)
    arg = list(func.free_symbols)[0]
    der = sp.lambdify(arg, sp.diff(func, arg))
    func = sp.lambdify(arg, func)

    k = 0
    gfk = der(x0)
    I = 1
    Hk = I
    xk = x0
    error_occured = False
    interim_results = pd.DataFrame(columns=['N', 'H', 'x_curr', 'x_next', 'p', 's', 'y'])
    flag = None
   
    while np.linalg.norm(gfk) > accuracy:
        if k >= max_iter:
            break
            
        pk = -np.dot(Hk, gfk)

        line_search = scipy.optimize.line_search(func, der, xk, pk, c1=c1, c2=c2)
        alpha_k = line_search[0]
        
        if alpha_k == None:
            error_occured = True
            break
        
        xkp1 = xk + alpha_k * pk
        sk = xkp1 - xk
        
        row = {
            'N': k,
            'H': Hk,
            'x_curr': xk,
            'p': pk,
            's': sk,
        }
        
        xk = xkp1
        row['x_next'] = xkp1
        
        gfkp1 = der(xkp1)
        yk = gfkp1 - gfk
        row['y'] = yk
        gfk = gfkp1
        
        interim_results = interim_results.append(row, ignore_index=True)
        
        if xkp1 > max_arg:
            flag = 3
            break
        
        k += 1
        
        ro = 1.0 / (np.dot(yk, sk))
        A1 = I - ro * sk * yk
        A2 = I - ro * yk * sk
        Hk = np.dot(A1, np.dot(Hk, A2)) + (ro * sk *sk)
        
    flag = 2 if k >= max_iter else flag
    flag = 4 if error_occured else flag
    if flag == None:
        flag = 0
    interim_results.set_index('N', inplace=True)
    if show_interim_results:
        display(HTML(interim_results.to_html()))
    result = {'arg': xk, 'func': func(xk), 'flag': flag}
    if return_data:
        result['data'] = interim_results
    return result


# In[8]:


def univariate_estimation(compare=False):
    """
    Создаёт интерактивный ввод и находит минимум вводимой функции выбранным методом
            Параметры:
                    compare (bool, default=False): 
                        Если True, выводит таблицу со сравнением решений задач всеми методами 
                        
            Возвращаемое значение:
                    result (dict):
                        Словарь, значениями которого являются точка минимума функции, значение функции в этой точке и флаг
                    
    """
    if compare:
        data = utils._take_input_univariate_estimation(1, 1)
        values = [['Полученное решение', 'Время выполнения (ms)', 'Количество итераций']]
        for algorithm in (golden_ratio, parabola_method, combined_brent, bfgs_method):
            start = time.time()
            if algorithm != bfgs_method:
                result = algorithm(
                    data['func'], data['bounds'], accuracy=data['accuracy'], max_iter=data['max_iter'],
                    return_data=True
                )
            else:
                result = algorithm(
                    data['func_str'], data['initial_point'], accuracy=data['accuracy'],
                    max_iter=data['max_iter'], max_arg=data['max_arg'], c1=data['c1'], c2=data['c2'],
                    return_data=True
                )
            if result['flag'] in (0, 1):
                solution = result['arg']
            else:
                solution = 'error occured'
            end = time.time()
            duration = end - start
            iter_num = len(result['data'].index)
            values.append([solution, duration, iter_num])
        acc_time_start = time.time()
        x1, x2 = data['bounds']
        acc_solution = scipy.optimize.fminbound(data['func'], x1, x2)
        acc_time_end = time.time()
        acc_duration = acc_time_end - acc_time_start
        values.append([acc_solution, acc_duration, '-'])
        fig = go.Figure(data=[go.Table(header=dict(values=['Параметр', 'метод золотого сечения', 'метод парабол', 'комбинированный метод Брента', 'BFGS', 'Оптимальный точный алгоритм']),
                 cells=dict(values=values))])
        fig.show()
        return
        
    else:
        method = int(input(
        """
        Выберите метод решения:
        1 - метод золотого сечения
        2 - метод парабол
        3 - комбинированный метод Брента
        4 - BFGS
        Метод: 
        """
        ))
        name_to_algo = {
            1: golden_ratio,
            2: parabola_method,
            3: combined_brent
        }
        show_interim_results = bool(int(input('Показать промежуточные результаты? 1-да / 0-нет: ')))
        if method in (1, 2, 3):
            show_convergency = bool(int(input('Показать график сходимости? 1-да / 0-нет: ')))
            data = utils._take_input_univariate_estimation(1, 0)
            return name_to_algo[method](
                data['func'], data['bounds'], accuracy=data['accuracy'], max_iter=data['max_iter'],
                show_interim_results=show_interim_results, show_convergency=show_convergency
            )
        else:
            data = utils._take_input_univariate_estimation(0, 1)
            return bfgs_method(
                data['func_str'], data['initial_point'], accuracy=data['accuracy'],
                max_iter=data['max_iter'], max_arg=data['max_arg'], c1=data['c1'], c2=data['c2'],
                return_data=True, show_interim_results=show_interim_results
            )



# In[9]:


#3------------------------------------------------------------


# In[10]:


def constant_gradient_descent(func, x0, alpha=0.1, max_iter=500, epsilon=1e-5, show_history=False, visualize=False):
    '''
    Находит точку минимума функции методом градиентного спуска с константным шагом.
            Параметры:
                    func (callable): 
                        Исследуемая функция
                    x0 (list): 
                        Начальная точка в виде списка координат
                    alpha (float, default=0.1): 
                        Размер шага градиентного спуска
                    max_iter (int, default=500): 
                        Максимальное количество итераций
                    epsilon (float, default=1e-5): 
                        Значение критеия останова
                    show_history (bool, default=False): 
                        Если True, выводит на экран промежуточные значения
                    visualize (bool, default=False)
                        Если True, строит график функции и движение градиентного спуска
                        
            Возвращаемое значение:
                    result (dict):
                        словарь, значениями которого являются найденная точка и значение функции в ней
                    history (pd.DataFrame):
                        датафрейм с промежуточными значениями
    '''
    x = np.array(x0, dtype=float)
    expr = sp.sympify(func)
    symbols = expr.free_symbols
    lambdifyed = sp.lambdify(symbols, expr)
    grad = utils._gradient(expr, x)
    f_x = lambdifyed(*x)
    history = pd.DataFrame({'Iter': [0], 'x': [x], 'f': f_x, '||grad||': [np.sum(grad**2)**0.5]})
    accuracy = int(np.log10(1/epsilon))
    
    for i in range(1, max_iter):
        if np.sum(grad**2)**0.5 < epsilon:
            history['code'] = 0
            break
        else:
            x = x - alpha * grad
            grad = utils._gradient(expr, x)
            f_x = lambdifyed(*x)

        row = {'Iter': i, 'x': x, 'f': f_x, '||grad||': np.sum(grad**2)**0.5}
        history = history.append(row, ignore_index=True)

    else:
        history['code'] = 1
        
    if show_history:
        for column in history.columns:
            if column != 'x':
                history[column] = [round(value, accuracy) for value in history[column]]
            else:
                history[column] = [[round(value, accuracy) for value in arr] for arr in history[column]]
        history.set_index('Iter', inplace=True)
        display(HTML(history.to_html()))
    
    if visualize:
        if len(x0) == 2:
            utils._visualize_gd(lambdifyed, history)

    return {'point': np.array([round(val, accuracy) for val in x]), 'f': round(f_x, accuracy)}, history


# In[11]:


def step_splitting_gd(func, x0, alpha0=0.1, delta=0.1, gamma=0.1, max_iter=500, epsilon=1e-5, show_history=False, visualize=False):
    '''
    Находит точку минимума функции методом градиентного спуска с дроблением шага.
            Параметры:
                    func (callable): 
                        Исследуемая функция
                    x0 (list): 
                        Начальная точка в виде списка координат
                    alpha0 (float, default=0.1): 
                        Размер начального шага градиентного спуска
                    delta (float, default=0.1):
                        Значение параметра оценки
                    gamma (float, default=0.1):
                        Значение параметра дробления
                    max_iter (int, default=500): 
                        Максимальное количество итераций
                    epsilon (float, default=1e-5): 
                        Значение критеия останова
                    show_history (bool, default=False): 
                        Если True, выводит на экран промежуточные значения
                    visualize (bool, default=False)
                        Если True, строит график функции и движение градиентного спуска
                        
            Возвращаемое значение:
                    result (dict):
                        словарь, значениями которого являются найденная точка и значение функции в ней
                    history (pd.DataFrame):
                        датафрейм с промежуточными значениями
    '''
    x = np.array(x0, dtype=float)
    expr = sp.sympify(func)
    symbols = expr.free_symbols
    lambdifyed = sp.lambdify(symbols, expr)
    grad = utils._gradient(expr, x)
    f_x = lambdifyed(*x)
    history = pd.DataFrame({'Iter': [0], 'x': [x], 'f': f_x, '||grad||': [np.sum(grad**2)**0.5]})
    accuracy = int(np.log10(1/epsilon))
    
    try:
        for i in range(1, max_iter):
            
            t = x - alpha0 * grad
            f_t = lambdifyed(*t)

            while not f_t - f_x <= - delta * alpha0 * sum(grad ** 2):
                alpha0 *= gamma
                t = x - gamma * grad
                f_t = lambdifyed(*t)

            x = t
            f_x = f_t
            grad = utils._gradient(expr, x)

            row = {'Iter': i, 'x': x, 'f': f_x, '||grad||': np.sum(grad**2)**0.5}
            history = history.append(row, ignore_index=True)
            
            if np.sum(grad**2)**0.5 < epsilon:
                history['code'] = 0
                break

        else:
            history['code'] = 1
            
    except Exception as e:
        history['code'] = 2
        
    if show_history:
        for column in history.columns:
            if column != 'x':
                history[column] = [round(value, accuracy) for value in history[column]]
            else:
                history[column] = [[round(value, accuracy) for value in arr] for arr in history[column]]
        history.set_index('Iter', inplace=True)
        display(HTML(history.to_html()))
        
    if visualize:
        if len(x0) == 2:
            utils._visualize_gd(lambdifyed, history)

    return {'point': np.array([round(val, accuracy) for val in x]), 'f': round(f_x, accuracy)}, history


# In[12]:


def fastest_gd(func, x0, max_iter=500, epsilon=1e-5, show_history=False, visualize=False):
    '''
    Находит точку минимума функции методом наискорейшего градиентного спуска.
            Параметры:
                    func (callable): 
                        Исследуемая функция
                    x0 (list): 
                        Начальная точка в виде списка координат
                    max_iter (int, default=500): 
                        Максимальное количество итераций
                    epsilon (float, default=1e-5): 
                        Значение критеия останова
                    show_history (bool, default=False): 
                        Если True, выводит на экран промежуточные значения
                    visualize (bool, default=False)
                        Если True, строит график функции и движение градиентного спуска
                        
            Возвращаемое значение:
                    result (dict):
                        словарь, значениями которого являются найденная точка и значение функции в ней
                    history (pd.DataFrame):
                        датафрейм с промежуточными значениями
    '''
    x = np.array(x0, dtype=float)
    expr = sp.sympify(func)
    symbols = expr.free_symbols
    lambdifyed = sp.lambdify(symbols, expr)
    grad = utils._gradient(expr, x)
    f_x = lambdifyed(*x)
    history = pd.DataFrame({'Iter': [0], 'x': [x], 'f': f_x, '||grad||': [np.sum(grad**2)**0.5]})
    accuracy = int(np.log10(1/epsilon))
    
    try:
        for i in range(1, max_iter):
            alpha = combined_brent(lambda lr: lambdifyed(*(x - lr*grad)), (0, 1))['arg']
            x = x - alpha * grad
            grad = utils._gradient(expr, x)
            f_x = lambdifyed(*x)

            row = {'Iter': i, 'x': x, 'f': f_x, '||grad||': np.sum(grad**2)**0.5}
            history = history.append(row, ignore_index=True)

            if np.sum(grad**2)**0.5 < epsilon:
                history['code'] = 0
                break

        else:
            history['code'] = 1
    
    except Exception as e:
        history['code'] = 2
        
    if show_history:
        for column in history.columns:
            if column != 'x':
                history[column] = [round(value, accuracy) for value in history[column]]
            else:
                history[column] = [[round(value, accuracy) for value in arr] for arr in history[column]]
        history.set_index('Iter', inplace=True)
        display(HTML(history.to_html()))

    if visualize:
        if len(x0) == 2:
            utils._visualize_gd(lambdifyed, history)

    return {'point': np.array([round(val, accuracy) for val in x]), 'f': round(f_x, accuracy)}, history


# In[13]:


def conjugate_gradient_method(func, x0, max_iter=500, epsilon=1e-5, show_history=False, visualize=False):
    '''
    Находит точку минимума функции методом Ньютона-сопряжённого градиента.
            Параметры:
                    func (callable): 
                        Исследуемая функция
                    x0 (list): 
                        Начальная точка в виде списка координат
                    max_iter (int, default=500): 
                        Максимальное количество итераций
                    epsilon (float, default=1e-5): 
                        Значение критеия останова
                    show_history (bool, default=False): 
                        Если True, выводит на экран промежуточные значения
                    visualize (bool, default=False)
                        Если True, строит график функции и движение градиентного спуска
                        
            Возвращаемое значение:
                    result (dict):
                        словарь, значениями которого являются найденная точка и значение функции в ней
                    history (pd.DataFrame):
                        датафрейм с промежуточными значениями
    '''
    x = np.array(x0, dtype=float)
    expr = sp.sympify(func)
    symbols = expr.free_symbols
    lambdifyed = sp.lambdify(symbols, expr)
    vectorized = lambda _x: lambdifyed(*x)
    grad = utils._gradient(expr, x)
    p = grad
    f_x = lambdifyed(*x)
    history = pd.DataFrame({'Iter': [0], 'x': [x], 'f': f_x, '||grad||': [np.sum(grad**2)**0.5]})
    accuracy = int(np.log10(1/epsilon)) 
    
    for i in range(1, max_iter):
        if np.sum(grad**2)**0.5 < epsilon:
            history['code'] = 0
            break
        else:
            alpha = line_search(vectorized, lambda _x: utils._gradient(expr, _x), x, p)[0]
            
            if alpha is None:
                alpha = combined_brent(lambda lr: lambdifyed(*(x - lr*p)), (0, 1))['arg']
                    
            x = x - alpha * p
            grad_new = utils._gradient(expr, x)
            beta_fr = (grad_new @ grad_new.reshape(-1, 1)) / (grad @ grad.reshape(-1, 1))
            p = grad_new + beta_fr * p
            grad = grad_new
            f_x = lambdifyed(*x)

        row = {'Iter': i, 'x': x, 'f': f_x, '||grad||': np.sum(grad**2)**0.5}
        history = history.append(row, ignore_index=True)

    else:
        history['code'] = 1
        
    if show_history:
        for column in history.columns:
            if column != 'x':
                history[column] = [round(value, accuracy) for value in history[column]]
            else:
                history[column] = [[round(value, accuracy) for value in arr] for arr in history[column]]
        history.set_index('Iter', inplace=True)
        display(HTML(history.to_html()))
        
    if visualize:
        if len(x0) == 2:
            utils._visualize_gd(lambdifyed, history)

    return {'point': np.array([round(val, accuracy) for val in x]), 'f': round(f_x, accuracy)}, history


# In[14]:


def compare_gd():
    '''
    Запрашивает у пользователя входные данные через и выводит на экран таблицу с результатами работы всех алгоритмов.
            Параметры:
                    None  
            Возвращаемое значение:
                    None
    '''
    data = utils._take_input_gd(1, 1, 1, 1)
    values = [['Полученное решение', 'Время выполнения (ms)', 'Количество итераций']]
    i_to_algo = {1: constant_gradient_descent, 2: step_splitting_gd,
                 3: fastest_gd, 4: conjugate_gradient_method}
    accuracy = -int(np.log10(data['epsilon']))
    
    for i in range(1, 5):
        algo = i_to_algo[i]
        start = time.time()
        if i == 1:
            res, history = algo(data['func'], data['x0'], data['alpha'], data['max_iter'],
                                data['epsilon'])
            
        elif i == 2:
            start = time.time()
            res, history = algo(data['func'], data['x0'], data['alpha0'], data['delta'], data['gamma'],
                                data['max_iter'], data['epsilon'])
            
        else:
            res, history = algo(data['func'], data['x0'], data['max_iter'],
                                data['epsilon'])
        
        end = time.time()
        duration = round(end - start, accuracy)
        solution = res['point']
        iter_num = len(history)
        values.append([solution, duration, iter_num])
        
    
    expr = sp.sympify(data['func'])
    symbols = expr.free_symbols
    lambdifyed = sp.lambdify(symbols, expr)
    acc_time_start = time.time()
    res = fmin(lambda _x: lambdifyed(*_x), data['x0'])
    acc_time_end = time.time()
    acc_duration = round(acc_time_end - acc_time_start, accuracy)
    solution = [round(x, accuracy) for x in res]
    values.append([solution, acc_duration, '-'])
    fig = go.Figure(data=[go.Table(header=dict(values=['Параметр', 'константный шаг', 'дробление шага', 'наискорейший спуск', 'Ньютон-сопряженный градиент', 'Оптимальный точный алгоритм']),
                                   cells=dict(values=values))])
    fig.show()


# In[15]:


def gradient_descent():
    '''
    Предлагает пользователю выбрать алгоритм решения, запрашивает у него данные и находит точку минимума, выбранным алгоритмом.
            Параметры:
                    None  
            Возвращаемое значение:
                    None
    '''
    method = int(input(
        """
        Выберите метод решения:
        1 - градиентный спуск с постоянным шагом
        2 - градиентный спуск с дроблением шага
        3 - наискорейший градиентный спуск
        4 - алгоритм Ньютона-сопряженного градиента
        Метод: 
        """
    ))
    if method == 1:
        data = utils._take_input_gd(ask_alpha=True, ask_history=True, ask_visualizing=True)
        return constant_gradient_descent(data['func'], data['x0'], data['alpha'], data['max_iter'],
                                         data['epsilon'], data['show_history'], data['visualize'])[0]
    elif method == 2:
        data = utils._take_input_gd(ask_alpha0=True, ask_delta=True, ask_gamma=True, ask_history=True, ask_visualizing=True)
        return step_splitting_gd(data['func'], data['x0'], data['alpha0'], data['delta'], data['gamma'],
                              data['max_iter'], data['epsilon'], data['show_history'], data['visualize'])[0]
    elif method == 3:
        data = utils._take_input_gd(ask_history=True, ask_visualizing=True)
        return fastest_gd(data['func'], data['x0'], data['max_iter'],
                                         data['epsilon'], data['show_history'], data['visualize'])[0]
    elif method == 4:
        data = utils._take_input_gd(ask_history=True, ask_visualizing=True)
        return conjugate_gradient_method(data['func'], data['x0'], data['max_iter'],
                                         data['epsilon'], data['show_history'], data['visualize'])[0]


# In[1]:


# 4----------------------------------------


# In[3]:


def Lin_reg(x, y, test_size =0.2, graph = False, in_pairs = False):
    '''
    Функция Lin_reg строит линейную регрессию для заданных данных.
        Параметры:
            x - pandas Датафрейм экзогенных переменных 
            x - pandas Датафрейм эндогенных переменных
            test_size - размер тестовой выборки. По умолчанию - 0.2
            graph - Если True, выводит график регрессии. По умолчанию - False
            in_pairs - Если True, строит парные регрессии для всех столбцов из x. По умолчанию -  False
            
    Функция возвраащает массив коэфициэнтов и свободный член регрессионной модели.
    
    
    '''
    x = pd.DataFrame(x)
    y = pd.DataFrame(y)
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=test_size)
    r2=[]
    if in_pairs:
        for i in x_train.columns:
            print(f'\nПарная регрессия для {y.columns[0]} и {i}')
            x_train1 = pd.DataFrame(x_train[i])
            y_train1 = pd.DataFrame(y_train)
            prm = LinearRegression()
            prm.fit(x_train1, y_train1)
            r2.append(r2_score(y_train1,prm.predict(x_train1)))
            print('Coef:',prm.coef_[0][0])
            print('Intercept:',prm.intercept_[0])
            print(f'R^2 for {i}: ', r2_score(y,prm.predict(pd.DataFrame(x[i]))))
            print('Mean squared error: ', mean_squared_error(y, prm.predict(pd.DataFrame(x[i]))))
            if graph:    
                fig, (ax1, ax2) = plt.subplots(1, 2, figsize = (12,4))
                ax1.scatter(x_train1, y_train1,color = 'green', alpha=0.7, label = 'Обучающая выборка')
                ax1.scatter(x_test[i], y_test,color = 'blue', alpha=0.7,label = 'Тестовая выборка')
                ax1.plot(x_train1,prm.predict(x_train1), color = 'red', linewidth = 2 )
                ax1.legend()
                ax2.scatter(x_test[i], y_test,color = 'blue', label = 'Тестовые данные')
                ax2.scatter(np.array(x_test[i]).reshape(-1,1), prm.predict(pd.DataFrame(x_test[i])),color = 'red', label = 'Прогноз модели')
                ax2.legend()
                plt.show() 
    prm = LinearRegression()
    prm.fit(pd.DataFrame(x_train),pd.DataFrame(y_train))
    print(f'\nМножественная линейная регрессия для {y.columns[0]} и X')
    print('Coef:',prm.coef_[0])
    print('Intercept:',prm.intercept_[0])
    print('R^2 for all X: ', prm.score(x,y))
    print('Mean squared error: ', mean_squared_error(y, prm.predict(x)))
    print('\n\n[MODEL] Y = ',end='')
    for i in range(len(x.columns)):
        print(round(prm.coef_[0][i],4),'*',x.columns[i],end = ' + ')
    print(round(prm.intercept_[0],3))
    if graph:    
        if len(x.columns[0])==2:
            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')
            ax.scatter(xs = x[x.columns[0]].values, ys =x[x.columns[1]].values, zs = y)
            ax.scatter(x[x.columns[0]].values, x[x.columns[1]].values,prm.predict(x).reshape(1,-1), color = 'r')
        if len(x.columns[0])==1:    
                fig, (ax1, ax2) = plt.subplots(1, 2, figsize = (12,4))
                ax1.scatter(x_train1, y_train1,color = 'green', alpha=0.7, label = 'Обучающая выборка')
                ax1.scatter(x_test[i], y_test,color = 'blue', alpha=0.7,label = 'Тестовая выборка')
                ax1.plot(x_train1,prm.predict(x_train1), color = 'red', linewidth = 2 )
                ax1.legend()
                ax2.scatter(x_test[i], y_test,color = 'blue', label = 'Тестовые данные')
                ax2.scatter(np.array(x_test[i]).reshape(-1,1), prm.predict(pd.DataFrame(x_test[i])),color = 'red', label = 'Прогноз модели')
                ax2.legend()
                plt.show() 

    return prm.coef_[0],prm.intercept_[0]


# In[4]:


def Poly_reg(x, y,test_size =0.2, degree = 2, graph = False):
    '''
        Функция Poly_reg строит парные полиномиальные регрессии для каждого х и y из заданных данных.
        Параметры:
            x - pandas Датафрейм экзогенных переменных 
            x - pandas Датафрейм эндогенных переменных
            test_size - размер тестовой выборки. По умолчанию - 0.2
            graph - Если True, выводит график регрессии. По умолчанию - False
            degree - Степень полинома. По умолчанию -  2
    
    '''
    x = pd.DataFrame(x)
    y = pd.DataFrame(y)
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=test_size)    
    y_train1 = pd.DataFrame(y_train)
    for i in x_train.columns:
        print(f'\nПолиномиальные регрессии {degree} порядка для {i}')
        x_train1 = pd.DataFrame(x_train[i])
        poly_reg = PolynomialFeatures(degree=degree)
        poly = poly_reg.fit_transform(x_train1) 
        new_reg = LinearRegression().fit(poly, y_train1)
        print('Coef:',new_reg.coef_[0][1:])
        print('Intercept:',new_reg.intercept_[0])
        print('Train data R^2:',new_reg.score(poly, y_train)) #train
        print('Test data R^2:',new_reg.score(poly_reg.fit_transform(pd.DataFrame(x_test[i])), y_test)) # test
        print('MSE:',mean_squared_error(y_train, new_reg.predict(poly)))
        print('MAE:',mean_absolute_error(y_train, new_reg.predict(poly)))
        if graph:
            fig = plt.figure()
            plt.scatter(x[i], y)
            plt.plot(x[i].sort_values(), new_reg.predict(poly_reg.fit_transform(x[i].sort_values().values.reshape((-1, 1)))), color='r')
            plt.show()


# In[16]:


# 5------------------------------------


# In[17]:


def inner_point():
    """
    Запрашивает у пользователя входную функцию, её аргументы, ограничения, начальную точку
    и находит точку экстремума при заданных ограничениях
     Параметры:
        None
     Возвращаемое значение:
        opt.x (np.array): координаты точки экстремума
     
    """
    func = input('Введите функцию в аналитическом виде: ')
    func = sympy.sympify(func)
    varnames = list(func.free_symbols)
    obj = utils.extract_coeffs(func, varnames)
    constraint = input('Введите хотя-бы одно ограничение (оставьте пустым для остановки):')
    lhs_ineq, rhs_ineq = [], []
    lhs_eq, rhs_eq = [], []
    while constraint:
        sign = re.findall(r'(?:<=|>=|=|<|>)', constraint)[0]
        left, right = constraint.split(sign)
        left = sympy.sympify(left)
        right = float(right)
        coeffs = dict()
        for var in varnames:
            coeffs[var] = left.coeff(var)
        if sign == '=':
            lhs_eq.append(list(coeffs.values()))
            rhs_eq.append([right])
        else:
            if sign in ('>=', '>'):
                right *= -1
                for var in coeffs:
                    coeffs[var] = -coeffs[var]
            lhs_ineq.append(list(coeffs.values()))
            rhs_ineq.append(right)
        

        constraint = input('Введите ограничение (оставьте пустым для остановки):')
    initial_point = list(map(float, input('Ввдите начальную точку: ').split()))
    lhs_ineq = lhs_ineq or None
    rhs_ineq = rhs_ineq or None
    lhs_eq = lhs_eq or None
    rhs_eq = rhs_eq or None
    opt = linprog(c=obj, A_ub=lhs_ineq, b_ub=rhs_ineq,
                  A_eq=lhs_eq, b_eq=rhs_eq, x0=initial_point,
                  method="revised simplex")
    return opt.x




# In[18]:


# 6--------------------------------------


# In[19]:


def logistic_regression(X_train, y_train, X_test, y_test, regularization=None, visualize=False):
    '''
    Классификатор, основанный на логистической регрессии.
            Параметры:
                    X_train (np.ndarray): 
                        массив признаков обучающей выборки
                    y_train (np.array): 
                        Вектор меток целевого признака обучающей выборки
                    X_test (np.ndarray): 
                        массив признаков тестовой выборки
                    y_test (np.array): 
                        Вектор меток целевого признака тестовой выборки
                    regularization {"l1", "l2", "None"}, default='None':
                        Параметр регуляризации
                    visualize (bool), default=False:
                        Если True, строит график классификации
                        
            Возвращаемое значение:
                    answer (dict):
                        Словарь, в котором хранятся предсказанные метки для тестовой выборки,
                        а также массив весов признаков
    '''
    if regularization is None:
        regularization = 'none'
    answer = dict()
    clf = LogisticRegression(solver='liblinear', penalty=regularization).fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    answer['predicted'] = y_pred
    coefs = clf.coef_[0]
    bias = clf.intercept_[0]
    answer['coefs'] = coefs
    answer['bias'] = bias
    if visualize and X_train.shape[1] == 2:
        plt.figure()
        plt.title('visualization of logistic regression')
        xmin, xmax = X_test[:, 0].min() - 1, X_test[:, 1].max() + 1
        ymin, ymax = X_test[:, 1].min() - 1, X_test[:, 1].max() + 1
        plt.xlim((xmin, xmax))
        plt.ylim((ymin, ymax))
        plt.scatter(X_test[:, 0], X_test[:, 1], c=y_test)
        ax = plt.gca()
        x_vals = np.array(ax.get_xlim())
        y_vals = -(x_vals * coefs[0] + bias)/coefs[1]
        plt.plot(x_vals, y_vals, '--', c="red")
    return answer


# In[20]:


def svm(X_train, y_train, X_test, y_test, visualize=False):
    '''
    Классификатор, основанный на векторе опорных векторов.
            Параметры:
                    X_train (np.ndarray): 
                        массив признаков обучающей выборки
                    y_train (np.array): 
                        Вектор меток целевого признака обучающей выборки
                    X_test (np.ndarray): 
                        массив признаков тестовой выборки
                    y_test (np.array): 
                        Вектор меток целевого признака тестовой выборки
                    visualize (bool), default=False:
                        Если True, строит график классификации
                        
            Возвращаемое значение:
                    answer (dict):
                        Словарь, в котором хранятся предсказанные метки для тестовой выборки,
                        а также массив весов признаков
    '''
    answer = dict()
    clf = SVC(kernel='linear').fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    answer['predicted'] = y_pred
    coefs = clf.coef_[0]
    bias = clf.intercept_[0]
    answer['coefs'] = coefs
    answer['bias'] = bias
    if visualize and X_train.shape[1] == 2:
        plt.figure()
        plt.title('visualization of logistic regression')
        ax = plt.gca()
        plt.scatter(X_train[:, 0], X_train[:, 1], c=y_train, s=50, cmap='autumn')
        xlim = ax.get_xlim()
        ylim = ax.get_ylim()

        xx = np.linspace(xlim[0], xlim[1], 30)
        yy = np.linspace(ylim[0], ylim[1], 30)
        YY, XX = np.meshgrid(yy, xx)
        xy = np.vstack([XX.ravel(), YY.ravel()]).T
        Z = clf.decision_function(xy).reshape(XX.shape)

        ax.contour(XX, YY, Z, colors='k', levels=[-1, 0, 1], alpha=0.5,
                   linestyles=['--', '-', '--'])

        ax.scatter(clf.support_vectors_[:, 0], clf.support_vectors_[:, 1], s=10,
                   linewidth=1, facecolors='none', edgecolors='k')
    return answer


# In[21]:


def compare_classification(X_train, y_train, X_test, y_test, regularization=None):
    '''
    Сравнивает показатели времени и точности различных классификаторов на одном наборе данных.
            Параметры:
                    X_train (np.ndarray): 
                        массив признаков обучающей выборки
                    y_train (np.array): 
                        Вектор меток целевого признака обучающей выборки
                    X_test (np.ndarray): 
                        массив признаков тестовой выборки
                    y_test (np.array): 
                        Вектор меток целевого признака тестовой выборки
                        
            Возвращаемое значение:
                    None
    '''
    start = time.time()
    log_reg_predict = logistic_regression(X_train, y_train, X_test, y_test, regularization=regularization)['predicted']
    log_reg_duration = time.time() - start
    start = time.time()
    svm_predict = svm(X_train, y_train, X_test, y_test)['predicted']
    svm_duration = time.time() - start
    log_reg_accuracy = accuracy_score(y_test, log_reg_predict)
    svm_accuracy = accuracy_score(y_test, svm_predict)
    values = [['accuracy', 'time(ms)'], [log_reg_accuracy, log_reg_duration], [svm_accuracy, svm_duration]]
    fig = go.Figure(data=[go.Table(header=dict(values=['', 'Logistic Regression', 'SVM']),
                                   cells=dict(values=values))])
    fig.show()



# In[6]:


def input_d():
  f=input('Введите функцию для решения задачи максимизации в аналитическом виде. Пример: x1+x2. Ввод:')
  g_count=input('Введите количество ограничений типа равенств. Пример: 2. Ввод:')
  g1=[]
  for i in range(int(g_count)):
    s='Введите ограничение f(x,y,z,...)=0. Пример: x1+x2-4. Ввод '+str(i+1)+':'
    g_=input(s)
    g1.append(g_)
  g_count=input('Введите количество ограничений типа неравенств. Пример: 2. Ввод:')
  g2=[]
  for i in range(int(g_count)):
    s='Введите ограничение f(x,y,z,...)<=0. Пример: x1+x2-4. Ввод '+str(i+1)+':'
    g_=input(s)
    g2.append(g_)
  return [f,g1,g2]


# In[7]:


def processing(s):
  f=parsing.sympy_parser.parse_expr(s[0])
  list_f=list(f.free_symbols)
  for g in s[1]:
    g=parsing.sympy_parser.parse_expr(g)
    list_f=list(set(list_f+list(g.free_symbols)))
  for g in s[2]:
    g=parsing.sympy_parser.parse_expr(g)
    list_f=list(set(list_f+list(g.free_symbols)))
  c=[]
  list_f.sort(key = default_sort_key)
  for x in list_f:
    c.append(float(f.diff(x)))
  c=c+[0]*len(s[2])
  A=[]
  b=[]
  for g in s[1]:
    g=parsing.sympy_parser.parse_expr(g)
    g_list=[]
    for x in list_f:
      g_list.append(float(g.diff(x)))
    const = float(g.func(*[term for term in g.args if not term.free_symbols]))
    g_list=g_list+[0]*len(s[2])
    A.append(g_list)
    b.append(-const)
  k=len(list_f)
  for g in s[2]:
    g=parsing.sympy_parser.parse_expr(g)
    g_list=[]
    for x in list_f:
      g_list.append(float(g.diff(x)))
    const = float(g.func(*[term for term in g.args if not term.free_symbols]))
    g_list=g_list+[0]*len(s[2])
    g_list[k]=1
    k+=1
    A.append(g_list)
    b.append(-const)
  return c,A,b,f,list_f


# In[8]:


def to_tableau(c, A, b):
    xb = [eq + [x] for eq, x in zip(A, b)]
    z = c + [0]
    return xb + [z]


# In[9]:


def can_be_improved(tableau):
    z = tableau[-1]
    return any(x > 0 for x in z[:-1])


# In[10]:


def get_pivot_position(tableau):
    z = tableau[-1]
    column = next(i for i, x in enumerate(z[:-1]) if x > 0)
    
    restrictions = []
    for eq in tableau[:-1]:
        el = eq[column]
        restrictions.append(math.inf if el <= 0 else eq[-1] / el)
        
    if (all([r == math.inf for r in restrictions])):
        print("Решение отсутствует.")
        return 0

    row = restrictions.index(min(restrictions))
    return row, column


# In[11]:


def pivot_step(tableau, pivot_position):
    new_tableau = [[] for eq in tableau]
    
    i, j = pivot_position
    pivot_value = tableau[i][j]
    new_tableau[i] = np.array(tableau[i]) / pivot_value
    
    for eq_i, eq in enumerate(tableau):
        if eq_i != i:
            multiplier = np.array(new_tableau[i]) * tableau[eq_i][j]
            new_tableau[eq_i] = np.array(tableau[eq_i]) - multiplier
   
    return new_tableau


# In[12]:


def is_basic(column):
    return sum(column) == 1 and len([c for c in column if c == 0]) == len(column) - 1


# In[13]:


def get_solution(tableau):
    columns = np.array(tableau).T
    solutions = []
    for column in columns[:-1]:
        solution = 0
        if is_basic(column):
            one_index = column.tolist().index(1)
            solution = columns[-1][one_index]
        solutions.append(solution)
        
    return solutions


# In[14]:


def simplex(c, A, b):
    tableau = to_tableau(c, A, b)

    while can_be_improved(tableau):
        pivot_position = get_pivot_position(tableau)
        tableau = pivot_step(tableau, pivot_position)

    return get_solution(tableau), tableau


# In[15]:


def gomori(c, A, b, f, list_f):
  solution, tableau = simplex(c, A, b)
  while len([c for c in solution if c%1==0]) != len(solution):
    remain=[]
    for sol in solution:
      remain.append(Fraction(sol).limit_denominator(1000)%1)
    rem_max=remain.index(max(remain))
    k=0
    for tab in tableau[:-1]:
      if solution[rem_max] in tab:
        tab_max=k
        break
      k+=1
    t_list=[]
    for t in tableau[tab_max][:-1]:
      if t<0:
        t_list.append(-(t-(int(t)-1)))
      if t>0:
        t_list.append(-(t-int(t)))
      if t==0:
        t_list.append(0)
    t_list.append(tableau[tab_max][-1]-int(tableau[tab_max][-1]))
    for i in range(len(tableau)):
      tableau[i]=np.array(list(tableau[i][:-1])+[0]+[tableau[i][-1]])
    a=tableau[-1]
    tableau[-1]=(np.array(list(t_list[:-1])+[1]+[-t_list[-1]]))
    tableau.append(a)
    tableau[-1][-1]=-tableau[-1][-1]
    teta=[]
    for i in range(len(tableau[-1])):
      if tableau[-2][i]==0:
        teta.append(10*10)
      else:
        teta.append(tableau[-1][i]/tableau[-2][i])
    teta_min=teta.index(min(teta[:-2]))
    tableau = pivot_step(tableau, (len(tableau)-2,teta_min))
    solution = get_solution(tableau)
    for i in range(len(solution)):
      solution[i]=round(solution[i],5)
  for i in range(len(solution)):
      solution[i]=round(solution[i])
  d_solve=dict(zip(list_f,solution[:len(list_f)]))
  d_solve_new=dict()
  for a in d_solve:
    if a in f.free_symbols:
      d_solve_new[a]=d_solve[a]
  print('Решением методом Гомори',d_solve_new,'max f =',f.subs(d_solve_new))


# In[17]:


def all_f_gomori():
  s=input_d()
  d=processing(s)
  gomori(*d)


# In[18]:


def branches_and_bound(c, A, b, last_sol):
  solution, tableau = simplex(c, A, b)
  sol=solution
  if solution==last_sol:
    return 'Ветка не подходит'
  else:
    for i in range(sum(np.array(c)!=0)):
      if solution[i]%1!=0:
          A_new1=A.copy()
          b_new1=b.copy()
          A_new2=A.copy()
          b_new2=b.copy()
          s1=[0]*len(solution)
          s2=[0]*len(solution)
          sol1=solution.copy()
          sol2=solution.copy()
          sol1[i]=math.trunc(sol1[i])
          sol2[i]=-(math.trunc(sol2[i])+1)
          s1[i]=1
          s2[i]=-1
          A_new1.append(s1)
          b_new1.append(sol1[i])
          A_new2.append(s2)
          b_new2.append(sol2[i])
          sol = [branches_and_bound(c, A_new1, b_new1, solution),branches_and_bound(c, A_new2, b_new2, solution)]
    return sol


# In[19]:


def unwrap_list(mylist, result):
   if any(isinstance(i, list) for i in mylist):
      for value in mylist:
         unwrap_list(value, result)
   else:
      result.append(mylist)


# In[20]:


def find_good(c,A,b,f,list_f,last_sol=[0]):
  solution = branches_and_bound(c,A,b,last_sol)
  result = []
  unwrap_list(solution, result)
  d=[]
  for sol in result:
    if sol!='Ветка не подходит':
      d.append(np.sum(np.array(c)*np.array(sol)))
  d_max=np.argmax(d)
  result=result[d_max]
  d_solve=dict(zip(list_f,result[:len(list_f)]))
  d_solve_new=dict()
  for a in d_solve:
    if a in f.free_symbols:
      d_solve_new[a]=d_solve[a]
  print('Решением методом ветвей и границ',d_solve_new,'max f =',f.subs(d_solve_new))


# In[21]:


def all_f_branches_and_bound():
  s=input_d()
  d=processing(s)
  find_good(*d)


# In[22]:


# 8------------------------------------------------------


# In[26]:


def SVM_SGD(X, Y, X_new, C=0.1, plot=False):
    '''
    Классификация на 2 класса методом опорных векторов с использованием градиентного спуска.
            Параметры:
                    X (np.ndarray): 
                        массив признаков обучающей выборки
                    Y (np.array): 
                        Вектор меток целевого признака обучающей выборки
                    X_new (np.ndarray): 
                        массив признаков тестовой выборки
                    C (float default=0.1): 
                        параметр регуляризации
                    plot (bool default=False):
                        Если True, визиализирует классификацию
                        
            Возвращаемое значение:
                    словарь с гипепараметрами и прогнозами для тестовых данных
    '''
    W = np.random.rand(2,1)
    b = np.random.rand()
    H_params = W,b
    lr=[1e-1,1e-3]
    n_iter = 200
    lr_diff = lr[1]-lr[0]
    loss="hinge"
    batch_size=50

    for t in tqdm(range(n_iter), leave=False):
        lr_t = (lr_diff/(n_iter-1))*t + lr[0]   # linear
        X_batch, Y_batch = utils.getBatch(X,Y,batch_size)
        delI_by_delW = np.zeros(W.shape)
        delI_by_delb = 0
        # sum the hinge loss gradients by looping over each sample
        for x,y in zip(X_batch,Y_batch):
            output = y*(np.dot(W.transpose(), x) + b)
            if loss in ["hinge", "sq_hinge"]:
                if output < 1:
                    if loss == "hinge":
                        delI_by_delW += -y*np.transpose([x])
                        delI_by_delb += -y
                elif loss == "sq_hinge":  # use smaller value of C for squared hinge loss
                    delI_by_delW += 2*(1-output)*(-y*np.transpose([x]))
                    delI_by_delb += 2*(1-output)*(-y)
            elif loss == "logistic":
                delI_by_delW += (-np.exp(output)/(1+np.exp(output)))*(-y*np.transpose([x]))
                delI_by_delb += (-np.exp(output)/(1+np.exp(output)))*(-y)

        delI_by_delW = delI_by_delW*len(X)/batch_size
        delI_by_delb = delI_by_delb*len(X)/batch_size

        delf_by_delW = W + C*delI_by_delW
        delf_by_delb = C*delI_by_delb

        W = W - lr_t*delf_by_delW
        b = b - lr_t*delf_by_delb
    
    Y_new = [-1 if pred <= 0 else 1 for pred in utils.predict(X_new.transpose(), (W, b))[0].tolist()]

    if plot:
        fig, ax = plt.subplots()
        ax.set_xlabel("x1");  ax.set_ylabel("x2")
        utils.plotHyperPlane(ax, X_new, Y_new,  (W,b))

    return {'W': W, 'b': b, 'Y_new': Y_new}


