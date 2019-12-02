from subprocess import run
from numpy import argmax, arange, pi, exp


import constants as const
import korp
import kan
from functions import config, find_coeff, find_macro, find_concent, draw
from commands import command


def lab5(d, delta, x_lst, gamma_fuel, gamma_cool,
         R_left=0.5, R_right=1.5, R_delta=0.025):
    R_array = arange(R_left, R_right, R_delta)
    result_dict = {}
    cool_compos = const.h2o_composition(gamma_cool)
    config('5')
    for x in x_lst:
        key = 'Обогащение '+str(x)
        result_dict[key] = {'K': [], 'Phi': [], 'Theta': [],
                            'AbsFuel': [], 'FisFuel': [], 'AbsMod': []}
        fuel_compos = const.uo2_composition(x, gamma_fuel)
        for R in R_array:
            file_in = open('lab5.txt', 'w')
            korp.create_file(file_in, d, delta, R, fuel_compos,
                             cool_compos, [command('fier', None),
                                           command('macro', '1,2,3,')])
            run('getera.exe')
            find_coeff('lab5.out', result_dict[key])
            find_macro('lab5.out', result_dict[key])
    draw('5', R_array, result_dict, 'Шаг решетки, см')
    return [R_array[argmax(result_dict[key]['K'])] for key in result_dict]


def lab6(d, delta, D, Delta, num_of_fuel_rods, x_lst, gamma_fuel,
         cool, mod, gamma_cool, gamma_mod, num_of_mod_rings,
         a_left=12, a_right=50, a_delta=1):
    # a^2 = pi*R^2 => R = a / sqrt(pi)
    a_array = arange(a_left, a_right, a_delta)
    R_array = a_array / pi**0.5
    result_dict = {}
    cool_compos = getattr(const, cool+'_composition')(gamma_cool)
    mod_compos = getattr(const, mod+'_composition')(gamma_mod)
    commands = [command('fier', None),
                command('macro', '2,1,2,3,1,2,3,2,' + '4,'*num_of_mod_rings)]
    config('6')
    for x in x_lst:
        key = 'Обогащение '+str(x)
        result_dict[key] = {'K': [], 'Phi': [], 'Theta': [],
                            'AbsFuel': [], 'FisFuel': [], 'AbsMod': []}
        fuel_compos = const.uo2_composition(x, gamma_fuel)
        for R in R_array:
            file_in = open('lab6.txt', 'w')
            kan.create_file(file_in, d, delta, R, D, Delta, num_of_fuel_rods,
                            num_of_mod_rings, fuel_compos, cool_compos,
                            mod_compos, commands)
            run('getera.exe')
            find_coeff('lab6.out', result_dict[key])
            find_macro('lab6.out', result_dict[key])
    draw('6', a_array, result_dict, 'Шаг решетки, см')
    return [R_array[argmax(result_dict[key]['K'])] for key in result_dict]


def lab7(d_korp, delta_korp, x_korp, gamma_fuel_korp, gamma_cool_korp, qv_korp,
         d_kan, delta_kan, D, Delta, num_of_fuel_rods, x_kan, gamma_fuel_kan,
         cool, mod, gamma_cool_kan, gamma_mod, num_of_mod_rings, qv_kan,
         time_step):
    def after_stop(time_array, flux, rho_array):
        time_array *= 3600*24
        exp_xe = exp(-const.lambda_xe * time_array)
        exp_i = exp(-const.lambda_i * time_array)
        coeff = ((const.lambda_xe + const.sigma_a_xe*flux) /
                 (const.lambda_xe - const.lambda_i))
        time_array /= 3600*24
        return (exp_xe + coeff*(exp_i - exp_xe))*rho_array[-1]/max(rho_array)

    def list_of_commands(qv, time_step):
        return [command('fier', None),
                command('burn', {'qv': str(qv), 'dtim': str(time_step)}),
                command('corr', None)]

    def command1(qv, time_step):
        return (list_of_commands(qv * 0.5, time_step) * int(1 / time_step) +
                list_of_commands(qv, time_step) * int(4 / time_step))

    def command2(qv, time_step):
        return (list_of_commands(qv, time_step) * int(4 / time_step) +
                list_of_commands(qv * 0.5, time_step) * int(1 / time_step))

    r_opt_korp = lab5(d_korp, delta_korp, [x_korp], gamma_fuel_korp,
                      gamma_cool_korp)[0]
    r_opt_kan = lab6(d_kan, delta_kan, D, Delta, num_of_fuel_rods, [x_kan],
                     gamma_fuel_kan, cool, mod, gamma_cool_kan,
                     gamma_mod, num_of_mod_rings)[0]
    fuel_compos_korp = const.uo2_composition(x_korp, gamma_fuel_korp)
    cool_compos_korp = getattr(const, cool+'_composition')(gamma_cool_korp)
    fuel_compos_kan = const.uo2_composition(x_kan, gamma_fuel_kan)
    cool_compos_kan = getattr(const, cool+'_composition')(gamma_cool_kan)
    mod_compos = getattr(const, mod+'_composition')(gamma_mod)
    for commands in [command1, command2]:
        key1, key2 = 'Корпусной', 'Канальный'
        result_dict = {}
        result_dict[key1] = {'K': []}
        result_dict[key2] = {'K': []}
        file_in = open('lab5.txt', 'w')
        korp.create_file(file_in, d_korp, delta_korp, r_opt_korp,
                         fuel_compos_korp, cool_compos_korp,
                         commands(qv_korp, time_step))
        config('5')
        run('getera.exe')
        find_coeff('lab5.out', result_dict[key1])
        find_concent('lab5.out', result_dict[key1])
        file_in = open('lab6.txt', 'w')
        kan.create_file(file_in, d_kan, delta_kan, r_opt_kan, D, Delta,
                        num_of_fuel_rods, num_of_mod_rings, fuel_compos_kan,
                        cool_compos_kan, mod_compos,
                        commands(qv_kan, time_step))
        config('6')
        run('getera.exe')
        find_coeff('lab6.out', result_dict[key2])
        find_concent('lab6.out', result_dict[key2])
        draw('7', arange(0, 5, time_step), result_dict, 'Время, сут')
