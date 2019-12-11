from subprocess import run
from numpy import interp, linspace, mean
from scipy.optimize import brentq

import constants as const
import korp
import kan
import functions as func
from commands import command, camp


def hw4(d, delta, x_u, x_pu, gamma_fuel, gamma_cool_korp, qv_korp,
        D, Delta, num_of_fuel_rods, cool, mod, gamma_cool_kan,
        gamma_mod, num_of_mod_rings, qv_kan):

    def continuous_overloads(k_func, right_b):
        b_array = linspace(0, right_b, 10)
        mean_k = mean([k_func(b) for b in b_array])
        return mean_k

    # создаем структуры данных
    key = ' '
    korp_dict = {key: {'K': [], 'u235': [const.param_uo2*gamma_fuel*x_u],
                       'pu39': [const.param_uo2*gamma_fuel*x_pu],
                       'pu40': [0], 'pu41': [0], 'pu42': [0], 'pu38': [0]}}
    # создаем материальные композиции корпусного реактора
    fuel_compos_korp = const.uo2_composition(x_u, x_pu, gamma_fuel)
    cool_compos_korp = getattr(const, 'h2o_composition')(gamma_cool_korp)
    # находим оптимальный шага решетки корпусного реактора
    r_opt_korp = func.find_r_opt_korp(d, delta, fuel_compos_korp,
                                      cool_compos_korp)
    # рассчитываем кампанию корпусного реактора
    file_in = open('lab5.txt', 'w')
    korp.create_file(file_in, d, delta, r_opt_korp,
                     fuel_compos_korp, cool_compos_korp, camp(qv_korp, 50, 25))
    func.config('5')
    run('getera.exe')
    # обрабатываем выходные данные
    func.find_coeff('lab5.out', korp_dict[key])
    func.find_concent('lab5.out', korp_dict[key], norm=False)
    burning_lst_korp = func.find_burning('lab5.out')
    # находим интересующее выгорание и отбрасываем лишние данные
    k_func = lambda b: interp(b, burning_lst_korp, korp_dict[key]['K'])
    result_func = lambda b: k_func(b) + k_func(2*b) + k_func(3*b) - 3
    end_burning = 3*brentq(result_func, 0, max(burning_lst_korp))
    func.clear_data(burning_lst_korp, end_burning, korp_dict[key])
    # создаем материальные композиции канального реактора
    fuel_compos_kan = func.find_compos('lab5.out', len(burning_lst_korp)-1, 1)
    fuel_compos_kan = {i: c for i, c in fuel_compos_kan.items()
                       if i != 'xe35' and c != 0}
    cool_compos_kan = getattr(const, cool+'_composition')(gamma_cool_kan)
    mod_compos = getattr(const, mod+'_composition')(gamma_mod)
    # создаем структуры данных
    kan_dict = {key: {'K': [], 'u235': [], 'pu39': [], 'pu40': [], 'pu41': [],
                      'pu42': [], 'pu38': []}}
    for var in kan_dict[key]:
        if var in fuel_compos_kan:
            kan_dict[key][var].append(fuel_compos_kan[var])
    # находим оптимальный шаг решетки канального реактора
    r_opt_kan = func.find_r_opt_kan(d, delta, D, Delta,
                                    num_of_fuel_rods, fuel_compos_kan,
                                    cool_compos_kan, mod_compos,
                                    num_of_mod_rings)
    # рассчитываем кампанию канального реактора
    file_in = open('lab6.txt', 'w')
    kan.create_file(file_in, d, delta, r_opt_kan, D, Delta,
                    num_of_fuel_rods, num_of_mod_rings, fuel_compos_kan,
                    cool_compos_kan, mod_compos, camp(qv_kan, 5, 25))
    func.config('6')
    run('getera.exe')
    # обрабатываем выходные данные
    func.find_coeff('lab6.out', kan_dict[key])
    func.find_concent('lab6.out', kan_dict[key], norm=False)
    burning_lst_kan = func.find_burning('lab6.out')
    # находим интересующее выгорание и отбрасываем лишние данные
    k_func = lambda b: interp(b, burning_lst_kan, kan_dict[key]['K'])
    result_func = lambda b: continuous_overloads(k_func, b) - 1
    end_burning = brentq(result_func, 0, max(burning_lst_kan))
    func.clear_data(burning_lst_kan, end_burning, kan_dict[key])
    # вывод результатов
    result_dict = korp_dict.copy()
    for var in result_dict[key]:
        result_dict[key][var] += kan_dict[key][var]
    burning = burning_lst_korp + list(map(lambda b: b + burning_lst_korp[-1],
                                          burning_lst_kan))
    func.draw('HW4', burning, result_dict,
              'Выгорание, '+r'$\frac{МВт\ сут}{кг}$')
