import matplotlib.pyplot as plt
from os import getcwd
from subprocess import run
from numpy import argmax, arange, pi

import korp
import kan
from commands import command


tex_dict = {'K': r'$K_{eff}$', 'Phi': r'$\varphi$', 'Theta': r'$\theta$',
            'AbsFuel': r'$\Sigma_a^{топ}$', 'FisFuel': r'$\Sigma_f^{топ}$',
            'AbsMod': r'$\Sigma_a^{зам}$', 'xe35': r'$Xe^{35}$',
            'pu38': r'$Pu^{238}$', 'pu39': r'$Pu^{239}$',
            'pu40': r'$Pu^{240}$', 'pu41': r'$Pu^{241}$',
            'pu42': r'$Pu^{242}$', 'u235': r'$U^{235}$'}
izotops = ['xe35', 'u235', 'pu38', 'pu39', 'pu40', 'pu41', 'pu42']


def config(num):
    config_file = open('CONFIG.DRV', 'r')
    help_list = []
    for line in config_file:
        help_list.append(line)
    config_file.close()
    config_file = open('CONFIG.DRV', 'w')
    for i, line in enumerate(help_list):
        if i == 8:
            config_file.write('INGET:lab' + num + '.txt\n')
        elif i == 9:
            config_file.write('OUTGET:lab' + num + '.out\n')
        else:
            config_file.write(line)
    config_file.close()


def find_coeff(name_of_file, result_dict):
    out_file = open(name_of_file, 'r')
    flag = False
    for line in out_file:
        if flag:
            help_list = line.split()
            if 'K' in result_dict:
                result_dict['K'].append(float(help_list[0]))
            if 'Phi' in result_dict:
                result_dict['Phi'].append(float(help_list[3]))
            if 'Theta' in result_dict:
                result_dict['Theta'].append(float(help_list[4]))
            flag = False
        elif 'keff' in line.split():
            flag = True


def find_concent(name_of_file, result_dict):

    def calcul_mean(lst):
        if lst == []:
            return 0
        mean_value = sum([(i + 1)*lst[i] for i in range(len(lst))])
        mean_value /= sum([i + 1 for i in range(len(lst))])
        return mean_value

    def normalize(result_dict):
        for izotop in izotops:
            if izotop in result_dict:
                max_c = max(result_dict[izotop])
                result_dict[izotop] = list(map(lambda c: c / max_c,
                                               result_dict[izotop]))

    def create_concent_dict(keys):
        concent_dict = {}
        for key in keys:
            if key in izotops:
                concent_dict[key] = []
        return concent_dict

    out_file = open(name_of_file, 'r')
    flag_out_data = False
    flag_corr_data = False
    concent_dict = create_concent_dict(result_dict.keys())
    for line in out_file:
        if flag_out_data:
            if flag_corr_data:
                help_list = line.split()
                for key in concent_dict:
                    if key in help_list:
                        concent_dict[key].append(float(help_list[2]))
            if line[:5] == ':corr':
                # фиксируем начало вывода результата команды corr
                flag_corr_data = True
            elif line[0] == ':' and flag_corr_data:
                # фиксируем окончание вывода результата команды corr
                flag_corr_data = False
                # обрабатываем найденные концентрации
                for key in concent_dict:
                    result_dict[key].append(calcul_mean(concent_dict[key]))
                    concent_dict[key] = []
        elif line[:5] == ':stop':
            # фиксируем окончание перечисления входных данных
            flag_out_data = True
    normalize(result_dict)


def find_macro(name_of_file, result_dict):
    out_file = open(name_of_file, 'r')
    flag = False
    counter = 1
    for line in out_file:
        if flag:
            help_list = line.split()
            if help_list[0] == '2':
                if counter == 1:
                    result_dict['AbsFuel'].append(float(help_list[3]))
                    result_dict['FisFuel'].append(float(help_list[5]))
                help_var = float(help_list[3])
                counter += 1
        elif '*grp*flux' in line.split():
            flag = True
    result_dict['AbsMod'].append(help_var)


def find_r_opt_korp(d, delta, fuel_compos, cool_compos, R_left=0.5,
                    R_right=1.5, R_delta=0.025):
    R_array = arange(R_left, R_right, R_delta)
    result_dict = {'K': []}
    config('5')
    for R in R_array:
        file_in = open('lab5.txt', 'w')
        korp.create_file(file_in, d, delta, R, fuel_compos,
                         cool_compos, [command('fier', None)])
        run('getera.exe')
        find_coeff('lab5.out', result_dict)
    return R_array[argmax(result_dict['K'])]


def find_r_opt_kan(d, delta, D, Delta, num_of_fuel_rods, fuel_compos,
                   cool_compos, mod_compos, num_of_mod_rings, a_left=12,
                   a_right=50, a_delta=1):
    # a^2 = pi*R^2 => R = a / sqrt(pi)
    a_array = arange(a_left, a_right, a_delta)
    R_array = a_array / pi**0.5
    result_dict = {'K': []}
    config('6')
    for R in R_array:
        file_in = open('lab6.txt', 'w')
        kan.create_file(file_in, d, delta, R, D, Delta, num_of_fuel_rods,
                        num_of_mod_rings, fuel_compos, cool_compos,
                        mod_compos, [command('fier', None)])
        run('getera.exe')
        find_coeff('lab6.out', result_dict)
    return R_array[argmax(result_dict['K'])]


def draw(num, step_array, result_dict, x_label):
    for name_of_var in tex_dict:
        if name_of_var not in result_dict[list(result_dict.keys())[0]]:
            continue
        plt.figure(figsize=(7, 7))
        for key in result_dict:
            plt.plot(step_array, result_dict[key][name_of_var],
                     label=key)
        plt.grid(True)
        plt.title(tex_dict[name_of_var])
        plt.xlabel(x_label, fontsize=15)
        plt.legend()
        plt.savefig(getcwd() + '\\ФТЯР\\LAB'+num+'\\' + name_of_var + '.png',
                    format='png', dpi=100)
        plt.clf()
