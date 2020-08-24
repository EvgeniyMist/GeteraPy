'''
Работа с модулем на примере лабораторных работ
'''


from os import listdir, mkdir, sep
from numpy import arange, linspace, pi

from rbase import draw, FileData, Matter
from wbase import Command, KanCell, KorpCell, Temp


STD_ET = [(1e+7, 2.15), (2.15, 0)]
# стандартные вещества
H2O = Matter('H2O', 0.7)
D2O = Matter('D2O', 1.1)
CARBON = Matter('C', 2.1)
UO2 = Matter('UO2', 10.4)
# стандартные параметры корпусного реактора
STD_KORP_QV = 110
STD_KORP_RANGE = arange(1.00, 3.05, 0.05)
STD_KORP_TEMP = Temp(1073, 593, 573, 0)
# стандартные параметры канального реактора
STD_D_ASSLY = 10
STD_DELTA_ASSLY = 0.25
STD_KAN_QV = 4.5
STD_KAN_RANGE = arange(12, 32.5, 0.5)
D2O_KAN_RANGE = arange(16, 36.5, 0.5)
D2O_KAN_TEMP = Temp(1773, 563, 543, 353)
STD_KAN_TEMP = Temp(1773, 563, 543, 873)
STD_NUM_OF_RINGS = 5
STD_NUM_OF_RODS = 18
# стандартные аргументы
DATA = (STD_NUM_OF_RODS, STD_D_ASSLY, STD_DELTA_ASSLY, None, STD_NUM_OF_RINGS)
D2O_KAN_DATA = DATA + (UO2, Matter('D2O', 0.7), D2O, D2O_KAN_TEMP)
STD_KAN_DATA = DATA + (UO2, H2O, CARBON, STD_KAN_TEMP)
STD_KORP_DATA = (None, UO2, H2O, STD_KORP_TEMP)


def case(string):
    ''' Изменяет окончание слов в полученной строке '''

    words = string.split()
    for i, word in enumerate(words):
        if word[-2:] == 'ый' or word[-2:] == 'ой':
            words[i] = word[:-2] + 'ого'
    return ' '.join(words)



def lab5(bin_path, d, delta):
    '''
    Аргументы:
        bin_path - путь к директории с исполняемым файлом getera.exe
        d        - диаметр твэла корпусного реактора, см
        delta    - толщина оболочки твэла корпусного реактора, см
    '''

    d /= 10
    delta /= 10

    res_path = bin_path + sep + 'lab5_result'
    if 'lab5_result' not in listdir(bin_path):
        mkdir(res_path)

    korp_cell = KorpCell(d, delta, *STD_KORP_DATA)
    korp_cell.bin_path = bin_path
    korp_cell.change_config()
    macro_data = {'NBV': [1, 2, 3], 'ET': STD_ET}
    commands = [Command('fier', None), Command('macro', macro_data)]
    data_lst = []
    x_tup = (0.036, 0.044)
    for x in x_tup:
        print('Расчет реактора при обогащении x = {:.3f}'.format(x), flush=True)
        data = FileData(korp_cell.out_abspath,
                        ['keff', 'fi', 'teta'], [], ['a', 'f'],
                        name='обогащение {:.3f}'.format(x))
        korp_cell.fuel = UO2
        korp_cell.fuel.add_uranium(x)
        for step in STD_KORP_RANGE:
            korp_cell.r_ex = step / 2
            korp_cell.create_and_run(commands)
            data.find_coeff()
            data.find_macro(zone_num=1)
        data_lst.append(data)
    print('Визуализация результатов расчета', flush=True)
    draw([STD_KORP_RANGE]*2, data_lst, 'Шаг решетки, см', res_path)
    print('Успешно', flush=True)


def lab6(bin_path, d, delta):
    '''
    Аргументы:
        bin_path - путь к директории с исполняемым файлом getera.exe
        d        - диаметр твэла канального реактора, см
        delta    - толщина оболочки твэла канального реактора, см
    '''

    d /= 10
    delta /= 10

    res_path = bin_path + sep + 'lab6_result'
    if 'lab6_result' not in listdir(bin_path):
        mkdir(res_path)

    for entry in [(0.02, 'std', 'водно-графитовый'),
                  (0.0071, 'd2o', 'тяжеловодный')]:
        x, code_name, name = entry
        if name not in listdir(res_path):
            mkdir(res_path + sep + name)
        print('Расчет %s реактора' % case(name), flush=True)
        data = globals()['%s_KAN_DATA' % code_name.upper()]
        kan_cell = KanCell(d, delta, *data)
        kan_cell.bin_path = bin_path
        kan_cell.change_config()
        nbv = [2] + [1, 2, 3]*kan_cell.num_of_rows + [2] + [4]*STD_NUM_OF_RINGS
        macro_data = {'NBV': nbv, 'ET': STD_ET}
        commands = [Command('fier', None),
                    Command('macro', macro_data)]
        data = FileData(kan_cell.out_abspath,
                        ['keff', 'fi', 'teta'], [], ['a', 'f'],
                        name=name)
        kan_cell.fuel = UO2
        kan_cell.fuel.add_uranium(x)
        for step in globals()['%s_KAN_RANGE' % code_name.upper()]:
            kan_cell.r_ex = step / pi**0.5
            kan_cell.create_and_run(commands)
            data.find_coeff()
            data.find_macro(zone_num=1)
        print('Визуализация результатов расчета', flush=True)
        draw([STD_KAN_RANGE, D2O_KAN_RANGE], [data], 'Шаг решетки, см',
             res_path + sep + name)
        print('Успешно', flush=True)


def lab7(bin_path, d_korp, delta_korp, d_kan, delta_kan):
    '''
    Аргументы:
        bin_path   - путь к директории с исполняемым файлом getera.exe
        d_korp     - диаметр твэла корпусного реактора, см
        delta_korp - толщина оболочки твэла корпусного реактора, см
        d_kan      - диаметр твэла канального реактора, см
        delta_kan  - толщина оболочки твэла канального реактора, см
    '''

    d_korp /= 10
    delta_korp /= 10
    d_kan /= 10
    delta_kan /= 10

    res_path = bin_path + sep + 'lab7_result'
    if 'lab7_result' not in listdir(bin_path):
        mkdir(res_path)

    step = 0.25
    x_dict = {'kan': 0.024, 'korp': 0.044}
    mod_param = [[(0.5, 4), (1, 16)], [(1, 16), (0.5, 4)]]
    data_lst = [[], []]
    for entry in [('kan', 'канальный'),
                  ('korp', 'корпусной')]:
        code_name, name = entry
        print('Расчет %s реактора' % case(name), flush=True)
        CellType = globals()['%sCell' % code_name.capitalize()]
        cell = CellType(locals()['d_%s' % code_name],
                        locals()['delta_%s' % code_name],
                        *globals()['STD_%s_DATA' % code_name.upper()])
        cell.fuel.add_uranium(x_dict[code_name])
        cell.bin_path = bin_path
        cell.find_r_opt(globals()['STD_%s_RANGE' % code_name.upper()])
        qv = globals()['STD_%s_QV' % code_name.upper()]
        for i, mod_data in enumerate(data_lst):
            mod_data.append(FileData(cell.out_abspath, [], ['xe35'], [],
                                     name=name))
            commands = []
            for tup in mod_param[i]:
                coeff, num_of_steps = tup
                commands += [Command('burn', {'qv': qv*coeff, 'dtim': step}),
                             Command('corr', None)]*num_of_steps
            cell.create_and_run(commands)
            mod_data[-1].find_bt()
            mod_data[-1].find_concent(cell.mean_func)
            mod_data[-1].normalize()
            cell.fuel = UO2
            cell.fuel.add_uranium(x_dict[code_name])
    print('Визуализация результатов расчета', flush=True)
    for i, mod_data in enumerate(data_lst):
        folder = 'mode%d' % i
        if folder not in listdir(res_path):
            mkdir(res_path + sep + folder   )
        x_data_lst = [data.bt_dict['time'] for data in mod_data]
        draw(x_data_lst, mod_data, r'Время, сут', res_path + sep + folder)
    print('Успешно', flush=True)


def lab8(bin_path, d_korp, delta_korp, d_kan, delta_kan):
    '''
    Аргументы:
        bin_path   - путь к директории с исполняемым файлом getera.exe
        d_korp     - диаметр твэла корпусного реактора, см
        delta_korp - толщина оболочки твэла корпусного реактора, см
        d_kan      - диаметр твэла канального реактора, см
        delta_kan  - толщина оболочки твэла канального реактора, см
    '''

    def calcul_gd():

        def add_gd(c):
            cell.fuel = UO2
            izotops = [('u238', 1 - x - c), ('u235', x), ('gd57', c)]
            cell.fuel.add_izotops({'u': izotops})

        k_lst = []
        c_range = linspace(10**-5, 10**-4, 20)
        for i, c in enumerate(c_range):
            add_gd(c)
            cell.create_and_run([Command('fier', None)])
            data = FileData(cell.out_abspath, ['keff'], [], [])
            data.find_coeff()
            k_lst.append(data.coeff_dict['keff'][0])
            if k_lst[i] < 1:
                add_gd(c_range[i-1])
                break
        cell.find_r_opt(globals()['STD_%s_RANGE' % code_name.upper()])

    d_korp /= 10
    delta_korp /= 10
    d_kan /= 10
    delta_kan /= 10

    res_path = bin_path + sep + 'lab8_result'
    if 'lab8_result' not in listdir(bin_path):
        mkdir(res_path)

    x = 0.03
    data_lst = []
    for entry in [('kan', 'канальный'),
                  ('korp', 'корпусной'),
                  ('korp', 'корпусной c Gd')]:
        code_name, name = entry
        print('Расчет %s реактора' % case(name), flush=True)
        CellType = globals()['%sCell' % code_name.capitalize()]
        cell = CellType(locals()['d_%s' % code_name],
                        locals()['delta_%s' % code_name],
                        *globals()['STD_%s_DATA' % code_name.upper()])
        cell.fuel.add_uranium(x)
        cell.bin_path = bin_path
        cell.find_r_opt(globals()['STD_%s_RANGE' % code_name.upper()])
        if 'gd' in name.lower():
            calcul_gd()
        data_lst.append(FileData(cell.out_abspath,
                                 ['keff'], ['u235', 'pu39', 'pu40'], [],
                                 name=name))
        qv = globals()['STD_%s_QV' % code_name.upper()]
        cell.calcul_camp(data_lst[-1], qv)
    print('Визуализация результатов расчета', flush=True)
    x_data_lst = [data.bt_dict['burn'] for data in data_lst]
    draw(x_data_lst, data_lst, r'$Выгорание, \frac{МВт \, сут}{кг}$',
               res_path)
    print('Успешно', flush=True)
