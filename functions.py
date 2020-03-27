import matplotlib.pyplot as plt
from os import getcwd

from commands import command


tex_dict = {'K': r'$K_{eff}$', 'Phi': r'$\varphi$', 'Theta': r'$\theta$',
            'AbsFuel': r'$\Sigma_a^{топ}$', 'FisFuel': r'$\Sigma_f^{топ}$',
            'AbsMod': r'$\Sigma_a^{зам}$', 'xe35': r'$Xe^{35}$',
            'pu38': r'$Pu^{238}$', 'pu39': r'$Pu^{239}$',
            'pu40': r'$Pu^{240}$', 'pu41': r'$Pu^{241}$',
            'pu42': r'$Pu^{242}$', 'u235': r'$U^{235}$'}
izotops = ['xe35', 'u235', 'pu38', 'pu39', 'pu40', 'pu41', 'pu42']


def camp(qv, time_step, num_of_step, initial_fier=True):
    ''' Возвращает список команд, необходимых для расчета кампании реактора

        Аргументы:
        qv - объемное энерговыделение
        time_step - величина шага по времени
        num_of_step - кол-во шагов
        при initial_fier = True в список команд будет включен также расчет
                           К в нулевой момент времени '''

    camp = [command('burn', {'qv': str(qv), 'dtim': str(time_step)}),
            command('corr', None), command('fier', None)]*num_of_step
    if initial_fier:
        return [command('fier', None)] + camp
    return camp


def clear_data(burning_lst, end_burning, result_dict):
    ''' Отсекает данные, соответствующие выгораниям, большим переданного
        значения end_burning

        Аргументы:
        burning_lst - список выгораний
        result_dict - стандартный словарь с данными '''

    for i in range(len(burning_lst)):
        if burning_lst[i] > end_burning:
            while len(burning_lst) != i:
                burning_lst.pop(i)
            for var in result_dict:
                result_dict[var] = result_dict[var][:i]
            return


def config(num):
    ''' Перезаписывает config файл, указывая в качестве входного и выходного
        файлов labn.txt и labn.out соответственно, где n - получаемый номер '''

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


def draw(folder, step, result_dict, x_label):
    ''' Визуализирует стандартный словарь с данным

        Аргументы:
        folder - название папки, в которую будут помещены изображения
        step - разбиение по оси абсцисс (в случае различных разбиений
                                         передается словарь)
        result_dict - стандартный словарь с данными
        x_label - подпись оси абсцисс '''

    for name_of_var in tex_dict:
        if name_of_var not in result_dict[list(result_dict.keys())[0]]:
            continue
        plt.figure(figsize=(7, 7))
        for key in result_dict:
            if isinstance(step, dict):
                x_array = step[key]
            else:
                x_array = step
            plt.plot(x_array, result_dict[key][name_of_var],
                     label=key)
        plt.grid(True)
        plt.title(tex_dict[name_of_var])
        plt.xlabel(x_label, fontsize=15)
        plt.legend()
        plt.savefig(getcwd() + '\\ФТЯР\\' + folder + '\\' + name_of_var +
                    '.png', format='png', dpi=100)
        plt.clf()


def find_burning(name_of_file):
    ''' Осуществляет поиск значений выгорания в выходном файле (name_of_file)
        и возвращает список из найденных значений '''

    out_file = open(name_of_file, 'r')
    burning_lst = []
    for line in out_file:
        if 'burn up' in line:
            burning_lst.append(float(line.split()[5]))
    burning_lst.insert(0, 0)
    return burning_lst


def find_coeff(name_of_file, result_dict):
    ''' Осуществляет поиск коэффициентов размножения и использования тепловых
        нейтронов, а также вероятность избежать резонансного поглощения
        и последующую их запись в переданную структуру данных

        Аргументы:
        name_of_file - название out-файла
        result_dict - стандартный словарь с данными '''

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


def find_compos(name_of_file, num_of_corr, num_of_cell):
    ''' Осуществляет поиск в выходном файле (name_of_file) и последующее
        возвращение изотопной компоции, соответсвутющей определенному номеру
        ячейки (num_of_cell) после определенной команды :corr (num_of_corr) '''

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
                try:
                    int(line.split()[0])
                except ValueError:
                    return compos
                compos[line.split()[1]] = float(line.split()[2])
        elif line[:5] == ':stop':
            # фиксируем окончание перечисления входных данных
            flag_out_data = True


def find_concent(name_of_file, result_dict, norm=True):
    ''' Осуществляет поиск концентраций изотопов и последующую их запись
        в переданную структуру данных

        Аргументы:
        name_of_file - название out-файла
        result_dict - стандартный словарь с данными
        при norm = True будет произведена нормировка концентраций каждого из
        изотопов на их максимальные значения '''

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
    if norm:
        normalize(result_dict)


def find_macro(name_of_file, result_dict):
    ''' Осуществляет поиск макроскопических сечений поглощения и деления
        топлива, поглощения замедлителя и последующую их запись в переданную
        структуру данных

        Аргументы:
        name_of_file - название out-файла
        result_dict - стандартный словарь с данными '''

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


def normalize(data):
    ''' Производит нормировку концентраций изотопов,
        находящихся в переданном словаре

        Аргументы:
        data - стандартный словарь с данными '''

    for izotop in izotops:
        if izotop in data:
            max_c = max(data[izotop])
            data[izotop] = list(map(lambda c: c / max_c, data[izotop]))
