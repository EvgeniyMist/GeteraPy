from subprocess import run
from numpy import arange, linspace, pi, exp, concatenate, interp
from scipy.optimize import brentq

import constants as const
import korp
import kan
import functions as func
from commands import command


def lab5(d, delta, x_lst, gamma_fuel, gamma_cool, r_left, r_right, r_delta):
    r_array = arange(r_left, r_right, r_delta)
    result_dict = {}
    cool_comp = const.h2o_composition(gamma_cool)
    func.config('5')
    for x in x_lst:
        key = 'Обогащение ' + str(x)
        result_dict[key] = {'K': [], 'Phi': [], 'Theta': [],
                            'AbsFuel': [], 'FisFuel': [], 'AbsMod': []}
        fuel_comp = const.uo2_composition(x, gamma=gamma_fuel)
        for r in r_array:
            file_in = open('lab5.txt', 'w')
            korp_cell = korp.KorpCell(d, delta, r, fuel_comp, cool_comp)
            commands = [command('fier', None), command('macro', '1, 2, 3,')]
            korp_cell.create_file(file_in, commands)
            run('getera.exe')
            func.find_coeff('lab5.out', result_dict[key])
            func.find_macro('lab5.out', result_dict[key])
    func.draw('Lab5', r_array, result_dict, 'Шаг решетки, см')


def lab6(d, delta, d_assly, delta_assly, fuel_rods_num, x_lst, gamma_fuel,
         cool, mod, gamma_cool, gamma_mod, mod_rings_num,
         a_left=12, a_right=50, a_delta=1):
        # a^2 = pi*R^2 => R = a / sqrt(pi)
    a_array = arange(a_left, a_right, a_delta)
    r_array = a_array / pi ** 0.5
    result_dict = {}
    if fuel_rods_num == 18:
        k = 2
    elif fuel_rods_num == 36:
        k = 3
    nbv = ('2, ' + '1, 2, 3, ' * k + '2, ' + '4, ' * mod_rings_num)
    cool_comp = getattr(const, cool+'_composition')(gamma_cool)
    mod_comp = getattr(const, mod+'_composition')(gamma_mod)
    commands = [command('fier', None), command('macro', nbv)]
    func.config('6')
    for x in x_lst:
        key = 'Обогащение '+str(x)
        result_dict[key] = {'K': [], 'Phi': [], 'Theta': [],
                            'AbsFuel': [], 'FisFuel': [], 'AbsMod': []}
        fuel_comp = const.uo2_composition(x, gamma=gamma_fuel)
        for r in r_array:
            file_in = open('lab6.txt', 'w')
            kan_cell = kan.KanCell(d, delta, fuel_rods_num, d_assly,
                                   delta_assly, r, mod_rings_num, fuel_comp,
                                   cool_comp, mod_comp)
            kan_cell.create_file(file_in, commands)
            run('getera.exe')
            func.find_coeff('lab6.out', result_dict[key])
            func.find_macro('lab6.out', result_dict[key])
    func.draw('Lab6', a_array, result_dict, 'Шаг решетки, см')


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
        return (func.camp(qv * 0.5, time_step, int(1 / time_step)) +
                func.camp(qv, time_step, int(4 / time_step), False))

    def mode2(qv, time_step):
        return (func.camp(qv, time_step, int(4 / time_step)) +
                func.camp(qv * 0.5, time_step, int(1 / time_step), False))

    # создание материальных композиций
    fuel_compos_korp = const.uo2_composition(x_korp, gamma=gamma_fuel_korp)
    cool_compos_korp = getattr(const, 'h2o_composition')(gamma_cool_korp)
    fuel_compos_kan = const.uo2_composition(x_kan, gamma=gamma_fuel_kan)
    cool_compos_kan = getattr(const, cool+'_composition')(gamma_cool_kan)
    mod_compos = getattr(const, mod+'_composition')(gamma_mod)
    # нахождение оптимальных радиусов
    r_opt_korp = func.find_r_opt_korp(d_korp, delta_korp, fuel_compos_korp,
                                      cool_compos_korp)
    r_opt_kan = func.find_r_opt_kan(d_kan, delta_kan, D, Delta,
                                    num_of_fuel_rods, fuel_compos_kan,
                                    cool_compos_kan, mod_compos,
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
    func.config('5')
    run('getera.exe')
    func.find_coeff('lab5.out', k_dict[key1])
    func.find_concent('lab5.out', xe_dict[key1])
    # расчет ячейки канального реактора
    file_in = open('lab6.txt', 'w')
    commands = locals()['mode'+str(mode)](qv_kan, time_step)
    kan.create_file(file_in, d_kan, delta_kan, r_opt_kan, D, Delta,
                    num_of_fuel_rods, num_of_mod_rings, fuel_compos_kan,
                    cool_compos_kan, mod_compos, commands)
    func.config('6')
    run('getera.exe')
    func.find_coeff('lab6.out', k_dict[key2])
    func.find_concent('lab6.out', xe_dict[key2])
    # вычисление концентрации ксенона после останова по теор. зависимости
    time_array = arange(0, 2, time_step/10)
    for concent in after_stop(time_array, 10**13, xe_dict[key1]['xe35']):
        xe_dict[key1]['xe35'].append(concent)
    for concent in after_stop(time_array, 7*10**12, xe_dict[key2]['xe35']):
        xe_dict[key2]['xe35'].append(concent)
    # вывод результатов
    func.draw('Lab7', arange(0, 5+time_step, time_step), k_dict, 'Время, сут')
    func.draw('Lab7', concatenate((arange(0, 5+time_step, time_step),
                                   arange(5, 7, time_step/10))),
              xe_dict, 'Время, сут')


def lab8(d_korp, delta_korp, x_korp, gamma_fuel_korp, gamma_cool_korp, qv_korp,
         d_kan, delta_kan, D, Delta, num_of_fuel_rods, x_kan, gamma_fuel_kan,
         cool, mod, gamma_cool_kan, gamma_mod, num_of_mod_rings, qv_kan):

    def find_gd(d, delta, r_opt, fuel_compos, cool_compos):

        def find_r(c, d, delta, r_opt, fuel_compos, cool_compos, commands):
            result_dict = {'K': []}
            fuel_compos['gd57'] = c*const.N_gd
            file_in = open('lab5.txt', 'w')
            korp.create_file(file_in, d, delta, r_opt, fuel_compos,
                             cool_compos, commands)
            run('getera.exe')
            func.find_coeff('lab5.out', result_dict)
            return result_dict['K'][0]

        commands = [command('fier', None)]
        gd_concent = linspace(10**-5, 10**-4, 10)
        k_lst = []
        for c in gd_concent:
            k_lst.append(find_r(c, d, delta, r_opt, fuel_compos, cool_compos,
                                commands))
        k_func = lambda c: interp(c, gd_concent, k_lst)
        result_func = lambda c: k_func(c) - 1
        return brentq(result_func, 10**-5, 10**-4)*const.N_gd

    # создание структур данных
    result_dict = {}
    key1, key2, key3 = 'Корпусной', 'Канальный', 'Корпусной с Gd'
    concent_u_korp = const.param_uo2*gamma_fuel_korp*x_korp
    concent_u_kan = const.param_uo2*gamma_fuel_korp*x_kan
    result_dict[key1] = {'K': [], 'pu39': [0], 'pu41': [0],
                         'u235': [concent_u_korp]}
    result_dict[key2] = {'K': [], 'pu39': [0], 'pu41': [0],
                         'u235': [concent_u_kan]}
    result_dict[key3] = {'K': [], 'pu39': [0], 'pu41': [0],
                         'u235': [concent_u_korp]}
    # расчет корпусного реактора
    commands = func.camp(qv_korp, 5, 1) + func.camp(qv_korp, 20, 40, False)
    fuel_compos_korp = const.uo2_composition(x_korp, gamma=gamma_fuel_korp)
    cool_compos_korp = getattr(const, 'h2o_composition')(gamma_cool_korp)
    korp_burning = func.camp_korp(d_korp, delta_korp, fuel_compos_korp,
                                  cool_compos_korp, commands,
                                  result_dict[key1])
    func.normalize(result_dict[key1])
    # расчет корпусного реактора c Gd
    fuel_compos_korp = const.uo2_composition(x_korp, gamma=gamma_fuel_korp)
    r_opt = func.find_r_opt_korp(d_korp, delta_korp, fuel_compos_korp,
                                 cool_compos_korp)
    fuel_compos_korp['gd57'] = find_gd(d_korp, delta_korp, r_opt,
                                       fuel_compos_korp, cool_compos_korp)
    korp_burning_gd = func.camp_korp(d_korp, delta_korp, fuel_compos_korp,
                                     cool_compos_korp, commands,
                                     result_dict[key3])
    func.normalize(result_dict[key3])
    # расчет корпусного реактора
    commands = func.camp(qv_kan, 5, 1) + func.camp(qv_kan, 50, 50, False)
    fuel_compos_kan = const.uo2_composition(x_korp, gamma=gamma_fuel_kan)
    cool_compos_kan = getattr(const, cool+'_composition')(gamma_cool_kan)
    mod_compos = getattr(const, mod+'_composition')(gamma_mod)
    kan_burning = func.camp_kan(d_kan, delta_kan, D, Delta, num_of_fuel_rods,
                                fuel_compos_kan, cool_compos_kan, mod_compos,
                                num_of_mod_rings, commands, result_dict[key2])
    func.normalize(result_dict[key2])
    # вывод результатов
    b_dict = {key1: korp_burning, key2: kan_burning, key3: korp_burning_gd}
    func.draw('Lab8', b_dict, result_dict, r'$Выгорание, \frac{МВт сут}{кг}$')
