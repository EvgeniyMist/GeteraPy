import matplotlib.pyplot as plt
from os import getcwd


tex_dict = {'K': r'$K_{eff}$', 'Phi': r'$\varphi$', 'Theta': r'$\theta$',
            'AbsFuel': r'$\Sigma_a^{топ}$', 'FisFuel': r'$\Sigma_f^{топ}$',
            'AbsMod': r'$\Sigma_a^{зам}$'}


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
        if 'keff' in line.split():
            flag = True


def find_concent(name_of_file, result_dict):
    pass


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
