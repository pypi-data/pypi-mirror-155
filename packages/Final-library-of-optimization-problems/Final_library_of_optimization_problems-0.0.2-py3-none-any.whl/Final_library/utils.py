#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sympy
import sympy as sp
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
import re
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from tqdm.notebook import tqdm
warnings.filterwarnings('ignore')


# In[2]:


# 1-----------------------------------------------------------------------------------


# In[3]:


def _take_input_extremas_searching(ask_restriction=False):
    '''
    Создаёт интерактивный ввод для пользователя и возвращает полученные данные в виде словаря.
            Параметры:
                    ask_restriction (bool): Если True, запрашивает у пользователя ограничивающую функцию
            Возвращаемое значение:
                    result (dict): Словарь, значениями которого являются введённые пользователем данные
    '''
    result = dict()
    result['varnames'] = list(input(f"Введите названия переменных\nПрим. x y: ").split())
    result['func'] = input('Введите функцию\nПрим. x**2 + y**2: ')
    is_bounded = int(input('Есть ли ограничения? 1-да, 0-нет: '))
    bounds = None
    if is_bounded:
        bounds = dict()
        for var in result['varnames']:
            bounds[var] = list(map(float, input(f'Введите допустимые интервалы по {var}: ').split()))
            
    if ask_restriction:
        result['restriction'] = input('Введите ограничивающую функцию: ')
        
    result['bounds'] = bounds
            
    return result


# In[4]:


def _get_hessian(func, args):
    '''
    Возвращает матрицу Гессе (вторых частных производных) входной функции по входным переменным.
            Параметры:
                    func (sympy.Expression): функция, по которой будут вычисляться частные производные
                    args (list[sympy.Symbol]): список, состоящий из переменных, по которым будут браться производные
            Возвращаемое значение:
                    result (sympy.Matrix): Матрица Гессе
    '''
    return sympy.Matrix([[func.diff(arg1, arg2) for arg1 in args] for arg2 in args])


# In[5]:


def _make_real(points, args):
    '''
    Функция проходит по всем входным точкам, и если у точки есть комплексное значение, оставляет только действительную часть 
            Параметры:
                    points (list): Список, состоящий из словарей (точек экстремумов)
                    args (list[sympy.Symbol]): список названий координат точек
            Возвращаемое значение:
                    result (dict): Словарь, значениями которого являются введённые пользователем данные
    '''
    result = []
    for point in list(points):
        for arg in args:
            if point[arg].has(sympy.I):
                point[arg] = sympy.re(point[arg])
        result.append(point)
    return result


# In[6]:


def _check_point(hesse, point):
    '''
    Функция делает вывод о типе экстремума входной точки с помощью определённости матрицы Гессе
            Параметры:
                    hesse (sympy.Matrix): Матрца Гессе
                    point (dict): Точка, тип экстремума которой проверяется
            Возвращаемое значение:
                    str: Вывод о типе экстремума
    '''
    substituted = hesse.subs(point)
    minor_dets = [substituted[:i, :i].det() for i in range(1, hesse.shape[0] + 1)]
    if all(det > 0 for det in minor_dets):
        return 'min'
    elif all(det < 0 for det in minor_dets[::2]) and all(det > 0 for det in minor_dets[1::2]):
        return 'max'
    elif minor_dets[-1] != 0:
        return 'saddle'
    else:
        return 'required additional research'


# In[7]:


def _filter_points(args, points, bounds):
    '''
    Отбирает те точки, которые лежат в пределах входных ограничений
            Параметры:
                    args (list[sympy.Symbol]): список названий координат точек
                    points (list): Список, состоящий из проверяемых точек
                    bounds (dict): Словарь, ключами которого являются названия осей, а ограничения значениями
            Возвращаемое значение:
                    suitable: Список, состоящий из отобранных точек
    '''
    suitable = []
    for point in points:
        is_suitable = True
        for arg in args:
            if not(bounds[arg.name][0] <= point[arg] <= bounds[arg.name][1]):
                is_suitable = False
        if is_suitable:
            suitable.append(point)
    return suitable


# In[8]:


def _plot(func, points, bounds=None, restriction=None):
    '''
    Строит график входной и ограничивающей (если задана) функции отображает точки экстремумов на ней
            Параметры:
                    func (sympy.Expression): функция, по которой будет построен график
                    points (list): Список, состоящий из точек экстремумов
                    bounds (dict): Словарь, ключами которого являются названия осей, а значениями
                                   ограничения, в пределах которого будет построен график
                    restriction (sympy.Expression): Ограничивающая функция
            Возвращаемое значение:
                    None
    '''
    args = list(func.free_symbols)
    arg1, arg2 = args
    if bounds:
        x, y = list(bounds.values())
        x = np.linspace(x[0], x[1], 100)
        y = np.linspace(y[0], y[1], 100)
    else:
        if points:
            x_min = min([point[arg1] for point in points]) - 2
            x_max = max([point[arg1] for point in points]) + 2
            y_min = min([point[arg2] for point in points]) - 2
            y_max = max([point[arg2] for point in points]) + 2
        else:
            x_min, x_max = -5, 5
            y_min, y_max = -5, 5
        x = np.linspace(x_min, x_max, 100)
        y = np.linspace(y_min, y_max, 100)
        
    x, y = np.meshgrid(x, y)
    z = sympy.lambdify(args, func)(x, y)
    scatters = []
    if points:
        colors = {
            'min': 'red',
            'max': 'green',
            'saddle': 'yellow'
        }
        for type_ in ('min', 'max', 'saddle'):
            required = [point for point in points if point['type']==type_]
            if not required:
                continue
            x_ = [point[arg1] for point in required]
            y_ = [point[arg2] for point in required]
            z_ = [point['F'] for point in required]
            curr_scatter = go.Scatter3d(x=x_, y=y_, z=z_,
                                        surfacecolor=colors[type_], mode='markers',
                                        marker=dict(color=colors[type_]), name=type_, showlegend=True)
            scatters.append(curr_scatter)
    surface = go.Surface(z=z, x=x, y=y, opacity=0.5, colorscale='inferno')
    figure = [surface] + scatters
    if restriction:
        restriction_z = sympy.lambdify(args, restriction)(x, y)
        figure.append(go.Surface(z=restriction_z, x=x, y=y, opacity=0.5, showscale=False, colorscale='ice'))
    fig = go.Figure(data=figure)
    fig.update_layout(title='3-D график функции с отмеченными точками локальных экстремумов.',
                      scene=dict(
                          xaxis_title=arg1.name,
                          yaxis_title=arg2.name,
                          zaxis_title=f'F({arg1}, {arg2})'),
                      legend=dict(x=0)
                      )
    fig.show()


# In[9]:


# 2------------------------------------------------------------------------------


# In[10]:


def _take_input_univariate_estimation(ask_bounds=False, ask_initial_point=False):
    '''
    Запрашивает у пользователя входные данные.
            Параметры:
                    ask_bounds (bool, default=False): 
                        Если True, запращивает у пользователя границы аргумента, точность метода
                        и макс. кол-во итераций
                    ask_initial_point (bool, default=False): 
                        Если True, запрашивает у пользователя начальную точку, первый и второй
                        параметр для условия Вольфе, а также максимальное ограничение по аргументу
                        
            Возвращаемое значение:
                    result (dict):
                        словарь, значениями которого являются введённые пользователем значения
    '''
    func_str = input('Введите функцию в аналитическом виде: ')
    func = sp.sympify(func_str)
    arg = list(func.free_symbols)[0]
    func = sp.lambdify(arg, func)
    result = {'func': func}
    result['func_str'] = func_str
    if ask_bounds:
        bounds = input('Введите ограничения по аргументу: ')
        bounds = tuple(map(float, map(sp.sympify, bounds.split())))
        result['bounds'] = bounds
        accuracy = input('Введите точность алгоритма (оставьте пустым для значения по умолчанию): ')
        accuracy = 10e-5 if not accuracy else float(accuracy)
        result['accuracy'] = accuracy
        max_iter = input('Введите макс. кол-во итераций (оставьте пустым для значения по умолчанию): ')
        max_iter = 500 if not max_iter else int(max_iter)
        result['max_iter'] = max_iter
    if ask_initial_point:
        initial_point = float(input('Введите начальную точку (для метода BFGS): '))
        result['initial_point'] = initial_point
        if result.get('accuracy', -1) == -1:
            accuracy = input('Введите точность алгоритма (оставьте пустым для значения по умолчанию): ')
            accuracy = 10e-5 if not accuracy else float(accuracy)
            result['accuracy'] = accuracy
            max_iter = input('Введите макс. кол-во итераций (оставьте пустым для значения по умолчанию): ')
            max_iter = 500 if not max_iter else int(accuracy)
            result['max_iter'] = max_iter
        c1 = input('Введите параметр для первого условия Вольфе (оставьте пустым для значения по умолчанию): ')
        c1 = 10e-4 if not c1 else float(c1)
        result['c1'] = c1
        c2 = input('Введите параметр для второго условия Вольфе (оставьте пустым для значения по умолчанию): ')
        c2 = 0.1 if not c2 else float(c2)
        result['c2'] = c2
        max_arg = input('Введите максимальное ограничение по аргументу (оставьте пустым для значения по умолчанию): ')
        max_arg = 100 if not max_arg else float(max_arg)
        result['max_arg'] = max_arg
    return result


# In[11]:


def _find_center(func, x1, x2, x3):
    '''
    Находит центр параболы, построенной по трём точкам.
            Параметры:
                    func (function): 
                        Исследуемая функция
                    x1 (float): 
                        Первая точка
                    x2 (float):
                        Вторая точка
                    x3 (float):
                        Третья точка
                        
            Возвращаемое значение:
                    center (float):
                        Координата центра параболы
    '''
    if (x1, func(x1)) == (x2, func(x2)) or (x2, func(x2)) == (x3, func(x3)) or (x1, func(x1)) == (x3, func(x3)):
        return
    f_1, f_2, f_3 = func(x1), func(x2), func(x3)
    a1 = (f_2 - f_1) / (x2 - x1)
    a2 = 1/(x3 - x2)*((f_3 - f_1)/(x3 - x1) - (f_2 - f_1)/(x2 - x1))
    center = 0.5*(x1 + x2 - a1/a2)
    return center


# In[12]:


def _show_convergency(data):
    '''
    Строит график сходимости алгоритма и выводит на экран размеры интервалов.
            Параметры:
                    data (list): 
                        Список значений размеров интервалов
                        
            Возвращаемое значение:
                    None
    '''
    print(data)
    plt.figure()
    plt.plot(list(range(len(data))), data)
    plt.xlabel('iter num')
    plt.ylabel('interval size')
    plt.title('convergency estimation')
    plt.show()


# In[13]:


# 3-------------------------------------------------------


# In[14]:


def _gradient(expr, point):
    '''
    Считает значение градиента функции в точке.
            Параметры:
                    expr (sympy.expression): 
                        функция, значение градиента которой считается
                    point (list): 
                        точка, в которой считается значение градиента
                        
            Возвращаемое значение:
                    grad (np.array):
                        numpy массив со значениями градиента
    '''
    grad = []
    symbols = list(expr.free_symbols)
    sub = dict(zip(symbols, point))
    for i in range(len(point)):
        curr_symbol = symbols[i]
        grad.append(expr.diff(curr_symbol).subs(sub))
    return np.array(grad, dtype=float)


# In[15]:


def _visualize_gd(func, history):
    '''
    Строит 3d график функции и scatter plot движения градиента.
            Параметры:
                    func (callable): 
                        функция, график которой строится
                    history (pd.DataFrame): 
                        датафрейм с промежуточными значеями
                        
            Возвращаемое значение:
                    None
    '''
    x_points = [point[0] for point in history['x']]
    y_points = [point[1] for point in history['x']]
    x_min, x_max = min(x_points), max(x_points)
    y_min, y_max = min(y_points), max(y_points)
    X = np.linspace(x_min, x_max, 100)
    Y = np.linspace(y_min, y_max, 100)
    X, Y = np.meshgrid(X, Y)
    Z = func(X, Y)
    scatter = data=go.Scatter3d(
        x=x_points, y=y_points, z=history['f'], mode='lines+markers', marker={'size':4})
    
    surface = go.Surface(z=Z, x=X, y=Y, opacity=0.5, colorscale='inferno')
    
    fig = go.Figure(data=[surface, scatter])
    
    fig.update_layout(title='График функции')
    fig.show()


# In[16]:


def _take_input_gd(ask_alpha=False, ask_alpha0=False, ask_delta=False, ask_gamma=False, ask_history=False, ask_visualizing=False):
    '''
    Запрашивает у пользователя входные данные.
            Параметры:
                    ask_alpha (bool, default=False): 
                        Если True, запращивает у пользователя константный шаг
                    ask_alpha0 (bool, default=False): 
                        Если True, запрашивает у пользователя начальный шаг
                    ask_delta (bool, default=False): 
                        Если True, запрашивает у пользователя значение параметра оценки
                    ask_gamma (bool, default=False): 
                        Если True, запрашивает у пользователя значение параметра дробления
                    ask_history (bool, default=False): 
                        Если True, спрашивает у пользователя, выводить ли промежуточные результаты?
                    ask_visualizing (bool, default=False): 
                        Если True, спрашивает у пользователя, визуализировать ли результаты?
                        
            Возвращаемое значение:
                    result (dict):
                        словарь, значениями которого являются введённые пользователем значения
    '''
    result = dict()
    func = input('Введите функцию в аналитическом виде: ')
    result['func'] = func
    x0 = list(map(float, input('Введите начальную точку: ').split()))
    result['x0'] = x0
    
    if ask_alpha:
        alpha = input('Введите константный шаг (оставьте пустым для значения по умолчанию):')
        alpha = 0.1 if not alpha else float(alpha)
        result['alpha'] = alpha
        
    if ask_alpha0:
        alpha0 = input('Введите начальный шаг (оставьте пустым для значения по умолчанию):')
        alpha0 = 0.1 if not alpha0 else float(alpha0)
        result['alpha0'] = alpha0
        
    if ask_delta:
        delta = input('Введите значение параметра оценки (оставьте пустым для значения по умолчанию): ')
        delta = 0.1 if not delta else float(delta)
        result['delta'] = delta
        
    if ask_gamma:
        gamma = input('Введите значение параметра дробления (оставьте пустым для значения по умолчанию): ')
        gamma = 0.1 if not gamma else float(gamma)
        result['gamma'] = gamma
        
    epsilon = input('Введите точность оптимизации (оставьте пустым для значения по умолчанию): ')
    epsilon = 1e-5 if not epsilon else float(epsilon)
    result['epsilon'] = epsilon
    max_iter = input('Введите максимальное количество итераций (оставьте пустым для значения по умолчанию): ')
    max_iter = 500 if not max_iter else int(max_iter)
    result['max_iter'] = max_iter
    
    if ask_history:
        show_history = bool(int(input('Показать промежуточные результаты? 1-да/0-нет: ')))
        result['show_history'] = show_history
        
    if ask_visualizing:
        visualize = bool(int(input('Визуализировать результат? 1-да/0-нет: ')))
        result['visualize'] = visualize
        
    return result


# In[17]:


# 5-------------------------------------------------------


# In[18]:


def extract_coeffs(expr, symbols):
    """
    Извлекает коэффициенты из sympy выражения
        Параметры:
            expr (sympy expression): уравнение или неравенство в виде sympy выражения
            symbols (List[sympy.Symbol]): список из переменных, коэффициенты перед которыми извлекаются
        Возвращаемое значение:
            res (List[float]): список коэффициентов
            
    """
    res = [float(expr.coeff(symbol)) for symbol in symbols]
    return res


# In[19]:


# 8-----------------------------------------------------


# In[20]:


def getBatch(X, Y, batch_size):
    '''
    Возвращает батчи входных данных.
            Параметры:
                    X (np.ndarray): 
                        массив признаков обучающей выборки
                    Y (np.array): 
                        Вектор меток целевого признака обучающей выборки
                    batch_size (int): 
                        размер батча
                        
            Возвращаемое значение:
                    X_batch (np.ndarray):
                        батч X
                    Y_batch (np.array):
                        батч Y
    '''
    batch_indxs = np.random.choice(len(X), size=batch_size, replace=False)
    X_batch = X[batch_indxs]
    Y_batch = Y[batch_indxs]
    return X_batch, Y_batch


# In[21]:


def predict(x, H_params):
    '''
    Возвращает предсказание для нового экземпляра.
            Параметры:
                    x (np.array): 
                        массив признаков нового экземпляра
                    H_params (tuple): 
                        кортеж с гиперпараметрами модели
                        
            Возвращаемое значение:
                    предсказание для нового экземпляра (float)
    '''
    W, b = H_params
    return (np.dot(W.transpose(), x) + b)


# In[22]:


def plotHyperPlane(ax, X, Y, H_params):
    '''
    Строит точки и разделяющие опорные вектора.
            Параметры:
                    ax : 
                        ось
                    X (np.ndarray): 
                        массив признаков обучающей выборки
                    Y (np.array): 
                        Вектор меток целевого признака обучающей выборки
                    H_params (tuple): 
                        кортеж с гиперпараметрами модели
                        
            Возвращаемое значение:
                    None
    '''
    x1min, x2min = np.min(X, axis=0)
    x1max, x2max = np.max(X, axis=0)
    xx = np.linspace(x1min, x1max, 10)
    yy = np.linspace(x2min, x2max, 10)

    X1, X2 = np.meshgrid(xx, yy)
    Z = np.empty(X1.shape)
    for (i, j), val in np.ndenumerate(X1):
        x1 = val
        x2 = X2[i, j]
        p = predict([[x1], [x2]], H_params)
        Z[i, j] = p[0]
    levels = [-1.0, 0.0, 1.0]
    linestyles = ['dashed', 'solid', 'dashed']
    colors = 'k'
    ax.contour(X1, X2, Z, levels, colors=colors, linestyles=linestyles)
    ax.scatter(X[:, 0], X[:, 1], c=Y, cmap=plt.cm.Paired,
               edgecolor='black', s=20)


# In[ ]:




