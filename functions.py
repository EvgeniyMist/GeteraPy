from os import getcwd, sep, listdir, mkdir
from collections import namedtuple
import matplotlib.pyplot as plt
from numpy import where, array


tex_dict = {'K': r'$K_{eff}$',
            'Phi': r'$\varphi$',
            'Theta': r'$\theta$',
            'AbsFuel': r'$\Sigma_a^{топ}$',
            'FisFuel': r'$\Sigma_f^{топ}$',
            'AbsMod': r'$\Sigma_a^{зам}$',
            'xe35': r'$Xe^{35}$',
            'pu38': r'$Pu^{238}$',
            'pu39': r'$Pu^{239}$',
            'pu40': r'$Pu^{240}$',
            'pu41': r'$Pu^{241}$',
            'pu42': r'$Pu^{242}$',
            'u235': r'$U^{235}$'}

izotops = ['xe35', 'u235', 'pu38', 'pu39', 'pu40', 'pu41', 'pu42']

Command = namedtuple('command', ['name', 'data'])


def camp(qv, time_step, num_of_steps, initial_fier=True):
    '''
    Возвращает список команд, необходимых для расчета кампании реактора

    Аргументы:
        qv - объемное энерговыделение
        time_step - величина шага по времени
        num_of_step - кол-во шагов
        при initial_fier = True в список команд будет включен также расчет
                           К в нулевой момент времени
    '''

    commands = [Command('burn', {'qv': str(qv), 'dtim': str(time_step)}),
                Command('corr', None), Command('fier', None)]*num_of_steps
    if initial_fier:
        return [Command('fier', None)] + commands
    return commands


def clear_data(burning_lst, end_burning, result_dict):
    '''
    Отсекает данные, соответствующие выгораниям, большим переданного значения

    Аргументы:
        burning_lst - список выгораний
        end_burning - максимальное значение выгорания
        result_dict - стандартный словарь с данными
    '''

    index = where(array(burning_lst) > end_burning)[0][0]
    for var in result_dict:
        result_dict[var] = result_dict[var][:index]
    while len(burning_lst) != index:
        burning_lst.pop()


def change_config(name):
    '''
    Перезаписывает config файл, указывая в качестве входного и выходного
    файлов name.txt и name.out соответственно

    Аргументы:
        name - название входного и выходного файлов
    '''

    unchanging_part = '''EDIT:cons.dat
                         EDIT0:..\\bin\\cons0.dat
                         BETA:..\\bin\\beta.get
                         BNAB.BIN:..\\bin\\Bnab90.lib
                         BNABMLT.BIN:..\\bin\\Bnabmlt.lib
                         BNABTHM.BIN:..\\bin\\BNABTHM.lib
                         BNAB:..\\bin\\XE35.MLT
                         F11:..\\bin\\f11\n'''
    unchanging_part = unchanging_part.replace('\t', '')
    unchanging_part = unchanging_part.replace(' ', '')
    config_file = open('CONFIG.DRV', 'w')
    config_file.write(unchanging_part)
    config_file.write('INGET:%s.txt\n' % name)
    config_file.write('OUTGET:%s.out\n' % name)
    config_file.close()


def draw(folder, step, result_dict, x_label):
    '''
    Визуализирует стандартный словарь с данным

    Аргументы:
        folder - название папки, в которую будут помещены изображения
        step - разбиение по оси абсцисс (в случае различных разбиений
                                         передается словарь)
        result_dict - стандартный словарь с данными
        x_label - подпись оси абсцисс
    '''

    lst_of_vars = result_dict[next(iter(result_dict))]
    for var in lst_of_vars:
        plt.figure(figsize=(7, 7))
        for key in result_dict:
            if isinstance(step, dict):
                x_array = step[key]
            else:
                x_array = step
            plt.plot(x_array, result_dict[key][var],
                     label=key)
        plt.grid(True)
        plt.title(tex_dict[var])
        plt.xlabel(x_label, fontsize=15)
        plt.legend()
        if folder not in listdir():
            mkdir(folder)
        path = getcwd() + sep + folder + sep
        plt.savefig('%s%s.png' % (path, var), format='png', dpi=100)
        plt.clf()


def find_burning(name_of_file):
    '''
    Осуществляет поиск значений выгорания в выходном файле
    и возвращает список из найденных значений

    Аргументы:
        name_of_file - название out-файла
    '''

    out_file = open(name_of_file, 'r')
    burning_lst = []
    for line in out_file:
        if 'burn up' in line:
            burning_lst.append(float(line.split()[5]))
    burning_lst.insert(0, 0)
    return burning_lst


def find_coeff(name_of_file, result_dict):
    '''
    Осуществляет поиск коэффициентов размножения и использования тепловых
    нейтронов, а также вероятность избежать резонансного поглощения
    и последующую их запись в переданную структуру данных

    Аргументы:
        name_of_file - название out-файла
        result_dict - стандартный словарь с данными
    '''

    out_file = open(name_of_file, 'r')
    flag = False
    for line in out_file:
        if flag:
            help_lst = line.split()
            if 'K' in result_dict:
                result_dict['K'].append(float(help_lst[0]))
            if 'Phi' in result_dict:
                result_dict['Phi'].append(float(help_lst[3]))
            if 'Theta' in result_dict:
                result_dict['Theta'].append(float(help_lst[4]))
            flag = False
        elif 'keff' in line.split():
            flag = True


def find_compos(name_of_file, num_of_corr, num_of_cell):
    '''
    Осуществляет поиск в выходном файле и последующее возвращение
    изотопной композиции, соответствующей определенному номеру ячейки
    после определенной команды :corr

    Аргументы:
        name_of_file - название out-файла
        num_of_corr - номер команды corr
        num_of_cell - номер ячейки
    '''

    out_file = open(name_of_file, 'r')
    flag_out_data = False
    flag_cell = False
    flag_data = False
    counter = 0
    compos = {}
    for line in out_file:
        if flag_out_data:
            if line[:5] == ':corr':
                # подсчитываем число команд corr
                counter += 1
            elif (counter == num_of_corr and 'number of cells' in line and
                  str(num_of_cell) in line):
                # фиксируем нахождение нужной ячейки в нужной по счету команде
                flag_cell = True
            elif flag_cell and 'izotop' in line:
                # фиксируем начало перечисления изотопного состава
                flag_data = True
            elif flag_data:
                help_lst = line.split()
                try:
                    int(help_lst[0])
                except ValueError:
                    break
                compos[help_lst[1]] = float(help_lst[2])
        elif line[:5] == ':stop':
            # фиксируем окончание перечисления входных данных
            flag_out_data = True
    return compos


def find_concent(name_of_file, result_dict, norm=True):
    '''
    Осуществляет поиск концентраций изотопов и последующую их запись
    в переданную структуру данных

    Аргументы:
        name_of_file - название out-файла
        result_dict - стандартный словарь с данными
        при norm = True будет произведена нормировка концентраций каждого из
                   изотопов на их максимальные значения
    '''

    def calcul_mean(lst):
        if lst == []:
            return 0
        mean_value = sum([(i + 1)*lst[i] for i in range(len(lst))])
        mean_value /= sum([i + 1 for i in range(len(lst))])
        return mean_value

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
                help_lst = line.split()
                for key in concent_dict:
                    if key in help_lst:
                        concent_dict[key].append(float(help_lst[2]))
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
    if norm:
        normalize(result_dict)


def find_macro(name_of_file, result_dict):
    '''
    Осуществляет поиск макроскопических сечений поглощения и деления
    топлива, поглощения замедлителя и последующую их запись в переданную
    структуру данных

    Аргументы:
        name_of_file - название out-файла
        result_dict - стандартный словарь с данными
    '''

    out_file = open(name_of_file, 'r')
    flag = False
    counter = 1
    for line in out_file:
        if flag:
            help_lst = line.split()
            if help_lst[0] == '2':
                if counter == 1:
                    result_dict['AbsFuel'].append(float(help_lst[3]))
                    result_dict['FisFuel'].append(float(help_lst[5]))
                help_var = float(help_lst[3])
                counter += 1
        elif '*grp*flux' in line.split():
            flag = True
    result_dict['AbsMod'].append(help_var)


def normalize(data, max_c_dict=None):
    '''
    Производит нормировку концентраций изотопов,
    находящихся в переданной структуре данных

    Аргументы:
        data - стандартный словарь с данными
        max_c_dict - структура данных, содержащая значения концентраций, на
                     которые будет произведена нормировка
    '''

    for izotop in izotops:
        if izotop in data:
            if max_c_dict is None:
                max_c = max(data[izotop])
            else:
                max_c = max_c_dict[izotop]
            data[izotop] = list(map(lambda c: c/max_c, data[izotop]))


def write_commands(file_in, commands):
    '''
    На основании переданного списка команд (commands) производит
    соответствующие записи во входной файл (file_in)
    '''

    def burn(file_in, data):
        file_in.write(':burn\n')
        file_in.write(' &vvod qv = %s dtim = %s &end\n' % (data['qv'],
                                                           data['dtim']))

    def corr(file_in, data):
        file_in.write(':corr\n')
        file_in.write(' &vvod &end\n')

    def fier(file_in, data):
        file_in.write(':fier\n')
        file_in.write(' &vvod &end\n')

    def macro(file_in, data):
        file_in.write(':macro\n')
        file_in.write(' &vvod\n')
        file_in.write('  ET = 10.5e+6,2.15, 2.15,0.,\n')
        file_in.write('  NBV = %s\n' % data)
        file_in.write(' &end\n')

    for cmd in commands:
        locals()[cmd.name](file_in, cmd.data)
    file_in.write(':stop\n')
