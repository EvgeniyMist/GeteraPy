'''
Модуль, предназначенный для извлечения, хранения и дальнейшей обработки
информации, находящейся в выходных файлах ПК Getera
'''


from os import sep
from warnings import warn
from bisect import bisect_left
from numpy import transpose
import matplotlib.pyplot as plt


# число Авгодаро
A = 0.6023  # 1/моль / 10^24

# молярные массы
MOLAR_MASS = {'h':   1.008,
              'd':   2.014,
              'he':  4.003,
              'b':  10.815,
              'c':  12.000,
              'n':  14.003,
              'o':  15.995,
              'al': 26.982,
              'zr': 91.224,
              'u': 238.051}


class Matter():
    '''
    Хранит необходимую для проведения расчета информацию о химическом веществе
    '''

    @property
    def comp(self):
        ''' Материальная композиция '''

        return self.__comp.copy()

    @property
    def density(self):
        ''' Плотность вещества'''

        return self.__density

    @density.setter
    def density(self, value):
        for izotop in self.__comp:
            self.__comp[izotop] *= value / self.__density
        self.__density = value

    @property
    def formula(self):
        ''' Химическая формула вещества'''

        return self.__formula

    @formula.setter
    def formula(self, value):
        self.__formula = value
        self.__create_comp()

    def __init__(self, formula, density, name=None, comp=None):
        '''
        Аргументы:
            formula : str   - химическая формула вещества
            density : float - плотность вещества, г/см^3
        Опциональные аргументы:
            name : str - название вещества
                по умолчанию совпадает с химической формулой
            comp : dict<str, float> - материальная композиция
                по умолчанию вычисляется исходя из хим. формулы и плотности
        '''

        self.__formula, self.__density = formula, density
        self.name = name if name is not None else formula
        if comp is not None:
            self.__comp = comp
        else:
            self.__create_comp()

    def add_izotops(self, data_dict):
        '''
        Производит добавление изотопов в материальную композицию вещества

        Аргументы:
            data_dict : dict<str, list<tuple<str, float>>>
                ключи    - входящие в вещество полиизотопные хим. элементы
                значения - пары, состоящие из изотопа и его отн. содержания
        '''

        for element in data_dict:
            element_concent = self.__comp.pop(element.lower())
            for data in data_dict[element]:
                izotop, prop = data
                self.__comp[izotop.lower()] = element_concent*prop

    def add_mod_prop(self):
        '''
        Кооректирует названия изотопов, выходящих в вещество, выполняющее
        функции замедлителя
        '''

        for element in self.comp:
            if element != 'd':
                self.add_izotops({element: [('*%s*' % element, 1)]})

    def add_uranium(self, x_u, x_pu=0.0):
        '''
        Производит замену урана на U238, U235 и Pu239

        Аргументы:
            x_u : float  - обогащение по U235, отн. ед.
            x_pu : float - обогащение по Pu239, отн. ед.
        '''

        izotops = [('u238', 1 - x_u - x_pu), ('u235', x_u)]
        if x_pu != 0:
            izotops.append(('pu39', x_pu))
        self.add_izotops({'u': izotops})

    def __create_comp(self):
        '''
        Создает удобную для дальнейшей работы структуру данных
        '''

        def update_comp(formula):
            if not formula[-1].isdigit():
                formula += '1'
            num = self.__comp.pop(formula[:-1].lower(), 0)
            self.__comp.update({formula[:-1].lower(): num + int(formula[-1])})

        self.__comp = {}
        last_index = 0
        for i, sym in enumerate(self.formula[1:]):
            if sym.isupper():
                update_comp(self.formula[last_index:i+1])
                last_index = i + 1
        update_comp(self.formula[last_index:])
        sub_mm = sum([num * MOLAR_MASS[elm] for elm, num in self.comp.items()])
        rho = A * self.density / sub_mm
        for element in self.comp:
            self.__comp[element] *= rho

class FileData():
    '''
    Обрабатывает информацию, находящуюся в выходных файлах Getera
    '''

    # обозначения величин в формуле 4-ех сомнож. и соотв. подписи к графикам
    COEFF_DICT = {'keff': r'$K_\infty$',
                  'nu': r'$\nu$',
                  'mu': r'$\mu$',
                  'fi': r'$\varphi$',
                  'teta': r'$\theta$'}
    # сообщение о несоответствии введенным обозначениям
    _COEFF_WARN = '''
%s не является обозначением какой-либо величины из формулы 4-ех сомножителей:
keff - коэффициент размножения
mu   - коэффициент размножения на быстрых нейтронах
fi   - вероятность избежать резонансного поглощения
teta - коэфициент использования тепловых нейтронов
nu   - среднее число нейтронов деления на один нейтрон, поглощенный в топл.'''

    # обозначения макроскопических констант и соотв. подписи к графикам
    MACRO_DICT = {'tot': r'$\Sigma_{tot}^{%d}$',
                  'a': r'$\Sigma_{a}^{%d}$',
                  'f': r'$\nu_{f}\Sigma_{f}^{%d}$',
                  's': r'$\Sigma_{s}^{%d \Rightarrow %d}$',
                  'D': r'$D^{%d}$'}
    # сообщение о несоответствии введенным обозначениям
    _MACRO_WARN = '''
%s не является обозначением какой-либо макроскопической константы:
tot - полное сечение
a   - сечение поглощения
f   - произведение среднего числа нейтронов на акт деления на сечение деления
s   - сечение рассеяния
D   - коэффициент диффузии'''

    def __init__(self, path_to_file, coefficients=[], izotops=[], constants=[],
                 name=None):
        '''
        Аргументы:
            path_to_file : str - путь к файлу с информацией
        Опциональные аргументы:
            coefficients : list<str> - необходимые "коэффициенты"
                по умолчанию отсутствуют
            izotops : list<str>      - необходимые изотопы
                по умолчанию отсутствуют
            constants : list<str>    - необходимые макроскопические константы
                по умолчанию отсутствуют
            name : str - подпись на графической интерпретации данных
                по умолчанию совпадает с названием файла с информацией
        '''

        self.path_to_file = path_to_file
        self.coeff_dict = {}
        self.__create_dict('coeff', coefficients)
        self.concent_dict = {izotop: [] for izotop in izotops}
        self.macro_dict = {}
        self.__create_dict('macro', constants)
        self.bt_dict = {'burn': [0], 'time': [0]}
        self.name = name if name is not None else ''

    def cut(self, end_burning=None, end_time=None):
        '''
        Отсекает данные, соотв. выгораниям или временам, большим заданных

        Опциональные аргументы:
            end_burning : float - максимальное значение выгорания
            end_time : int      - длительность кампании
        '''

        def get_index(x_lst, x_max):
            if x_max is None:
                return len(x_lst)
            return bisect_left(x_lst, x_max)

        index = min(get_index(self.bt_dict['time'], end_time),
                    get_index(self.bt_dict['burn'], end_burning))
        result_dict = {}
        result_dict.update(**self.coeff_dict, **self.concent_dict,
                           **self.macro_dict, **self.bt_dict)
        for key in result_dict:
            while len(result_dict[key]) != index:
                result_dict[key].pop()

    def draw(self, x_data):
        '''
        Визуализирует данные

        Аргументы:
            x_data : str - откладываемые по оси абсцисс значения
        '''

        def plot_q(q_name, y_data, title):
            plt.figure(q_name, figsize=(7, 7))
            plt.plot(x_data, y_data, label=self.name)
            plt.title(title)

        for coeff in self.coeff_dict:
            plot_q(coeff, self.coeff_dict[coeff], self.COEFF_DICT[coeff])
        for izotop in self.concent_dict:
            i = ([sym.isdigit() for sym in izotop] + [True]).index(True)
            plot_q(izotop, self.concent_dict[izotop],
                   r'$\rho(%s^{%s})$' % (izotop[:i], izotop[i:]))
        for macro, value in self.macro_dict.items():
            if macro == 's':
                continue
            for i, group_macro in enumerate(transpose(value)):
                plot_q(macro + str(i), group_macro,
                       self.MACRO_DICT[macro] % (i + 1))

    def find_bt(self):
        '''
        Осуществляет поиск и последующее добавление значений выгорания и
        моментов времени, для которых был произведен расчет
        '''

        out_file = open(self.path_to_file, 'r')
        for line in out_file:
            if line[:5] == ':burn':
                next(out_file)
                self.bt_dict['time'].append(self.bt_dict['time'][-1] +
                                            int(next(out_file).split()[2]))
            elif line[:5] == ':stop':
                break
        for line in out_file:
            if line[:5] == ':burn':
                self.bt_dict['burn'].append(float(next(out_file).split()[5]))
        out_file.close()

    def find_coeff(self):
        '''
        Осуществляет поиск и последующее добавление значений "коэффициентов"
        '''

        out_file = self.__find_stop()
        for line in out_file:
            if line.split() == list(self.COEFF_DICT.keys()):
                coeff_dict = dict(zip(self.COEFF_DICT.keys(),
                                      map(float, next(out_file).split())))
                for coeff in self.coeff_dict:
                    self.coeff_dict[coeff].append(coeff_dict[coeff])
        out_file.close()

    def find_comp(self, corr_num, cell_num, zone_num, clear=True):
        '''
        Осуществляет поиск материальной композиции, соответствующей заданной
        зоне заданной ячейки после заданной команды :corr, и последующее
        создание экземпляра класса Matter

        Аргументы:
            corr_num : int - номер команды corr
            cell_num : int - номер ячейки
            zone_num : int - номер зоны
        Опциональные аргументы:
            clear : bool   - удаление изотопов с нулевой концентрацией
                по умолчанию True
        Возвращаемое значение:
            экземляр класса Matter, содержащий найденную мат. композицию и
            информацию об ее источнике
        '''

        out_file = self.__find_stop()
        corr_counter = 0
        cell_counter = 0
        comp = {}
        for line in out_file:
            if line[:5] == ':corr':
                corr_counter += 1
            elif corr_counter == corr_num and 'izotop' in line:
                cell_counter += 1
                if cell_counter == cell_num:
                    help_lst = next(out_file).split()
                    while help_lst[0].isdigit():
                        izotop = help_lst[1]
                        concent = float(help_lst[1+zone_num])
                        if not clear or concent != 0:
                            comp[izotop] = concent
                        help_lst = next(out_file).split()
                    break
        name = 'Zone%d_Cell%d_Corr%d' % (zone_num, cell_num, corr_num)
        out_file.close()
        return Matter(None, None, name, comp)

    def find_concent(self, mean_func):
        '''
        Осуществляет поиск и последующее добавление концентраций изотопов

        Аргументы:
            mean_func : callable<list<float>> - усредняет конц. по полиячейке
                в качестве аргумента получает список конц. в ячейках
        '''

        out_file = self.__find_stop()
        corr_flag = False
        for line in out_file:
            if corr_flag and 'izotop' in line:
                for lst in self.concent_dict.values():
                    lst[-1].append(0)
                help_lst = next(out_file).split()
                while help_lst[0].isdigit():
                    izotop = help_lst[1]
                    if izotop in self.concent_dict:
                        concent = next(num for num in map(float, help_lst[2:])
                                       if num != 0)
                        self.concent_dict[izotop][-1][-1] = concent
                    line = next(out_file)
                    help_lst = line.split()
            if ':corr' in line or ':poly' in line:
                corr_flag = True
                for lst in self.concent_dict.values():
                    lst.append([])
            elif line[0] == ':' and corr_flag:
                corr_flag = False
                for lst in self.concent_dict.values():
                    lst[-1] = mean_func(lst[-1])
        out_file.close()

    def find_macro(self, zone_num):
        '''
        Осуществляет поиск и последующее добавление макроскопических констант

        Аргументы:
            zone_num : int - номер зоны,
                             усредненные константы по которой будут найдены
        '''

        macro_dict = {macro: [] for macro in self.MACRO_DICT}
        out_file = self.__find_stop()
        zone_count = 0
        macro_flag = False
        for line in out_file:
            if macro_flag and 'n zone' in line:
                zone_count += 1
                if zone_count == zone_num:
                    num_of_groups = 0
                    next(out_file)
                    help_lst = next(out_file).split()
                    while help_lst[0].isdigit():
                        num_of_groups += 1
                        help_lst = list(map(float, help_lst))
                        macro_dict['tot'][-1].append(help_lst[2])
                        macro_dict['a'][-1].append(help_lst[3])
                        macro_dict['f'][-1].append(help_lst[5])
                        macro_dict['D'][-1].append(help_lst[6])
                        help_lst = next(out_file).split()
                    next(out_file)
                    for _ in range(num_of_groups):
                        help_lst = list(map(float, next(out_file).split()[2:]))
                        macro_dict['s'][-1].append(help_lst)
            if ':macro' in line:
                macro_flag = True
                for lst in macro_dict.values():
                    lst.append([])
            elif line[0] == ':' and macro_flag:
                zone_count = 0
                macro_flag = False
        for macro in self.macro_dict:
            self.macro_dict[macro].extend(macro_dict[macro])
        out_file.close()

    def normalize(self, max_c_dict={}):
        '''
        Производит нормировку концентраций изотопов

        Опциональные аргументы:
            max_c_dict : dict<str, float>
                ключи    - изотопы
                значения - величины, на которые будет произведена нормировка
        '''

        for izotop in self.concent_dict:
            if izotop in max_c_dict:
                max_c = max_c_dict[izotop]
            else:
                max_c = max(self.concent_dict[izotop])
            for i in range(len(self.concent_dict[izotop])):
                self.concent_dict[izotop][i] /= max_c

    def __create_dict(self, attr, keys):
        for key in keys:
            if key in getattr(self, attr.upper() + '_DICT'):
                getattr(self, attr + '_dict').update({key: []})
            else:
                warn(getattr(self, '_' + attr.upper() + '_WARN') % key)

    def __find_stop(self):
        out_file = open(self.path_to_file, 'r')
        for line in out_file:
            if line[:5] == ':stop':
                break
        return out_file


def draw(x_data_lst, y_data_lst, x_label, path):
    '''
    Визуализирует набор данных

    Аргументы:
        x_data_lst : list<list<float>> - откладываемые по оси асбсцисс зн-ия
        y_data_lst : list<FileData>    - набор данных
        x_label : str                  - подпись оси абсцисс
        path : str                     - путь сохранения изображений
    '''

    for x_data, y_data in zip(x_data_lst, y_data_lst):
        y_data.draw(x_data)
    for i in plt.get_fignums():
        plt.figure(i)
        plt.grid()
        plt.xlabel(x_label)
        plt.legend()
        plt.savefig(path + sep + '%d.png' % i, format='png', dpi=100)
        plt.clf()
