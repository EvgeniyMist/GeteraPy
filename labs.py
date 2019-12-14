from subprocess import run
from numpy import arange, pi, exp, concatenate

import constants as const
import korp
import kan
from functions import*
from commands import command, camp


def lab5(d, delta, x_lst, gamma_fuel, gamma_cool, R_left, R_right, R_delta):
    R_array = arange(R_left, R_right, R_delta)
    result_dict = {}
    cool_compos = const.h2o_composition(gamma_cool)
    config('5')
    for x in x_lst:
        key = 'Обогащение '+str(x)
        result_dict[key] = {'K': [], 'Phi': [], 'Theta': [],
                            'AbsFuel': [], 'FisFuel': [], 'AbsMod': []}
        fuel_compos = const.uo2_composition(x, gamma=gamma_fuel)
        for R in R_array:
            file_in = open('lab5.txt', 'w')
            korp.create_file(file_in, d, delta, R, fuel_compos,
                             cool_compos, [command('fier', None),
                                           command('macro', '1, 2, 3,')])
            run('getera.exe')
            find_coeff('lab5.out', result_dict[key])
            find_macro('lab5.out', result_dict[key])
    draw('Lab5', R_array, result_dict, 'Шаг решетки, см')


def lab6(d, delta, D, Delta, num_of_fuel_rods, x_lst, gamma_fuel,
         cool, mod, gamma_cool, gamma_mod, num_of_mod_rings,
         a_left=12, a_right=50, a_delta=1):
    # a^2 = pi*R^2 => R = a / sqrt(pi)
    a_array = arange(a_left, a_right, a_delta)
    R_array = a_array / pi**0.5
    result_dict = {}
    if num_of_fuel_rods == 18:
        k = 2
    elif num_of_fuel_rods == 36:
        k = 3
    nbv = ('2, ' + '1, 2, 3, ' * k + '2, ' + '4, ' * num_of_mod_rings)
    cool_compos = getattr(const, cool+'_composition')(gamma_cool)
    mod_compos = getattr(const, mod+'_composition')(gamma_mod)
    commands = [command('fier', None), command('macro', nbv)]
    config('6')
    for x in x_lst:
        key = 'Обогащение '+str(x)
        result_dict[key] = {'K': [], 'Phi': [], 'Theta': [],
                            'AbsFuel': [], 'FisFuel': [], 'AbsMod': []}
        fuel_compos = const.uo2_composition(x, gamma=gamma_fuel)
        for R in R_array:
            file_in = open('lab6.txt', 'w')
            kan.create_file(file_in, d, delta, R, D, Delta, num_of_fuel_rods,
                            num_of_mod_rings, fuel_compos, cool_compos,
                            mod_compos, commands)
            run('getera.exe')
            find_coeff('lab6.out', result_dict[key])
            find_macro('lab6.out', result_dict[key])
    draw('Lab6', a_array, result_dict, 'Шаг решетки, см')


def lab7(d_korp, delta_korp, x_korp, gamma_fuel_korp, gamma_cool_korp, qv_korp,
         d_kan, delta_kan, D, Delta, num_of_fuel_rods, x_kan, gamma_fuel_kan,
         cool, mod, gamma_cool_kan, gamma_mod, num_of_mod_rings, qv_kan,
         time_step, mode):

    def after_stop(time_array, flux, rho_array):
        time_array *= 3600*24
        exp_xe = exp(-const.lambda_xe * time_array)
        exp_i = exp(-const.lambda_i * time_array)
        coeff = ((const.lambda_xe + const.sigma_a_xe*flux) /
                 (const.lambda_xe - const.lambda_i))
        time_array /= 3600*24
        return (exp_xe + coeff*(exp_i - exp_xe))*rho_array[-1]/max(rho_array)

    def mode1(qv, time_step):
        return (camp(qv * 0.5, time_step, int(1 / time_step)) +
                camp(qv, time_step, int(4 / time_step), False))

    def mode2(qv, time_step):
        return (camp(qv, time_step, int(4 / time_step)) +
                camp(qv * 0.5, time_step, int(1 / time_step), False))

    # создание материальных композиций
    fuel_compos_korp = const.uo2_composition(x_korp, gamma=gamma_fuel_korp)
    cool_compos_korp = getattr(const, 'h2o_composition')(gamma_cool_korp)
    fuel_compos_kan = const.uo2_composition(x_kan, gamma=gamma_fuel_kan)
    cool_compos_kan = getattr(const, cool+'_composition')(gamma_cool_kan)
    mod_compos = getattr(const, mod+'_composition')(gamma_mod)
    # нахождение оптимальных радиусов
    r_opt_korp = find_r_opt_korp(d_korp, delta_korp, fuel_compos_korp,
                                 cool_compos_korp)
    r_opt_kan = find_r_opt_kan(d_kan, delta_kan, D, Delta, num_of_fuel_rods,
                               fuel_compos_kan, cool_compos_kan, mod_compos,
                               num_of_mod_rings)
    # создание структур данных
    key1, key2 = 'Корпусной', 'Канальный'
    k_dict = {key1: {'K': []}, key2: {'K': []}}
    xe_dict = {key1: {'xe35': [0]}, key2: {'xe35': [0]}}
    # расчет ячейки копусного реактора
    file_in = open('lab5.txt', 'w')
    commands = locals()['mode'+str(mode)](qv_korp, time_step)
    korp.create_file(file_in, d_korp, delta_korp, r_opt_korp,
                     fuel_compos_korp, cool_compos_korp, commands)
    config('5')
    run('getera.exe')
    find_coeff('lab5.out', k_dict[key1])
    find_concent('lab5.out', xe_dict[key1])
    # расчет ячейки канального реактора
    file_in = open('lab6.txt', 'w')
    commands = locals()['mode'+str(mode)](qv_kan, time_step)
    kan.create_file(file_in, d_kan, delta_kan, r_opt_kan, D, Delta,
                    num_of_fuel_rods, num_of_mod_rings, fuel_compos_kan,
                    cool_compos_kan, mod_compos, commands)
    config('6')
    run('getera.exe')
    find_coeff('lab6.out', k_dict[key2])
    find_concent('lab6.out', xe_dict[key2])
    # вычисление концентрации ксенона после останова по теор. зависимости
    time_array = arange(0, 2, time_step/10)
    for concent in after_stop(time_array, 10**13, xe_dict[key1]['xe35']):
        xe_dict[key1]['xe35'].append(concent)
    for concent in after_stop(time_array, 7*10**12, xe_dict[key2]['xe35']):
        xe_dict[key2]['xe35'].append(concent)
    # прорисовка
    draw('Lab7', arange(0, 5+time_step, time_step), k_dict, 'Время, сут')
    draw('Lab7', concatenate((arange(0, 5+time_step, time_step),
                              arange(5, 7, time_step/10))),
        xe_dict, 'Время, сут')
