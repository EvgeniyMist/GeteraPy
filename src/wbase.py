'''
Модуль, предназначенный для создания входных файлов ПК Getera и
его автоматизированного запуска
'''


from os import path, sep
from subprocess import DEVNULL, run
from warnings import warn
from copy import deepcopy
from abc import ABC, abstractmethod
from collections import namedtuple
from numpy import argmax, interp, linspace, pi, sqrt
from scipy.optimize import brentq

import rbase


# цирконий
zr = rbase.Matter('Zr', 6.506)

# структура данных, хранящая температуры материалов
Temp = namedtuple('Temp', ('fuel', 'shell', 'cool', 'mod'))

# структура данных, хранящая информацию о вводимой команде
Command = namedtuple('command', ['name', 'data'])


class Cell(ABC):
    '''
    Абстрактная ячейка
    '''

    __CAMP_WARN = '''
Не удалось рассчитать кампанию реактора со следующими параметрами:
step = %d, сут
num_of_steps = %d'''

    __WORK_FOLDER = 'work_dir' + sep

    @property
    def bin_path(self):
        ''' путь к директории с исполняемым файлом getera.exe '''

        return self.__bin_path

    @bin_path.setter
    def bin_path(self, value):
        self.__bin_path = value

    @property
    def cool(self):
        ''' Теплоноситель '''

        return self.__cool

    @cool.setter
    def cool(self, value):
        self.__cool = deepcopy(value)
        self.__cool.add_mod_prop()

    @property
    def fuel(self):
        ''' Топливо '''

        return self.__fuel

    @fuel.setter
    def fuel(self, value):
        self.__fuel = deepcopy(value)

    @property
    @abstractmethod
    def init_step(self):
        ''' Величина начального шага расчета кампании, сут '''

    @property
    @abstractmethod
    def inp_file(self):
        ''' Название входного файла '''

    @property
    @abstractmethod
    def num_of_steps(self):
        ''' Количество стандартных шагов расчета кампании реактора '''

    @property
    def out_abspath(self):
        ''' Абсолютный путь выходного файла '''

        return self.bin_path + sep + self.__WORK_FOLDER + self.out_file

    @property
    @abstractmethod
    def out_file(self):
        ''' Название выходного файла '''

    @property
    def r_ex(self):
        ''' Внешний радиус ячейки '''

        return self.__r_ex

    @r_ex.setter
    def r_ex(self, value):
        self.__r_ex = value

    @property
    @abstractmethod
    def step(self):
        ''' Величина стандартного шана расчета кампании, сут '''

    def calcul_camp(self, data, qv):
        '''
        Выполняет расчет кампании реактора

        Аргументы:
            data : base.FileData - хранилище информации
            qv : int             - объемное энерговыделение, кВт/л
        '''

        def camp_commands(time_step, num_of_steps):
            return [Command('burn', {'qv': qv, 'dtim': time_step}),
                    Command('corr', None), Command('fier', None)]*num_of_steps

        self.change_config()
        self.create_and_run([Command('fier', None)] +
                            camp_commands(self.init_step, 1) +
                            camp_commands(self.step, self.num_of_steps))
        data.find_bt()
        data.find_coeff()
        data.find_concent(self.mean_func)
        k_func = lambda b: interp(b, data.bt_dict['burn'],
                                  data.coeff_dict['keff'])
        result_func = lambda b: self.camp_func(b, k_func)
        try:
            end_burning = brentq(result_func, data.bt_dict['burn'][0],
                                 data.bt_dict['burn'][-1])
        except ValueError:
            warn(self.__CAMP_WARN % (self.step, self.num_of_steps))
            end_burning = data.bt_dict['burn'][-1]
        data.cut(end_burning)

    @abstractmethod
    def camp_func(self, b, k_func):
        '''
        Функция, задающая кампанию реактора

        Аргументы:
            b : float - выгорание мВт*сут/кг
            k_func : callable<float> - задает коэффициент размножения
                в качестве аргмуента принимает выгорание
        '''

    def change_config(self):
        '''
        Перезаписывает config файл, изменяя в нем входной и выходной файлы
        '''

        unchanging_part = '''EDIT:cons.dat
EDIT0:cons0.dat
BETA:beta.get
BNAB.BIN:bnab90.lib
BNABMLT.BIN:bnabmlt.lib
BNABTHM.BIN:bnabthm.lib
BNAB:xe35.mlt
F11:f11\n'''

        in_str = 'INGET:{}\n'.format(self.__WORK_FOLDER + self.inp_file)
        out_str = 'OUTGET:{}\n'.format(self.__WORK_FOLDER + self.out_file)
        with open(self.bin_path + sep + 'config.drv', 'w') as config_file:
            config_file.write(unchanging_part)
            config_file.write(in_str)
            config_file.write(out_str)

    def create_and_run(self, commands):
        '''
        Создает входной файл для расчета

        Аргументы:
            commands : list<Command> - необходимые для расчета команды
        '''


        file_in_path = self.bin_path + sep + self.__WORK_FOLDER + self.inp_file
        with open(file_in_path, 'w') as file_in:
            self._before_concent(file_in)
            self._concent(file_in)
            self._after_concent(file_in)
            self._write_commands(file_in, commands)
        run(self.bin_path + sep + 'getera.exe', check=True, cwd=self.bin_path,
            stdout=DEVNULL)

    def find_r_opt(self, r_array):
        '''
        Вычисляет оптимальный радиус ячейки

        Аргументы:
            r_array - проверяемые радиусы
        '''

        self.change_config()
        data = rbase.FileData(self.out_abspath, ['keff'])
        for r in r_array:
            self.r_ex = r
            self.create_and_run([Command('fier', None)])
            data.find_coeff()
        self.r_ex = r_array[argmax(data.coeff_dict['keff'])]

    @abstractmethod
    def mean_func(self, lst):
        '''
        Выполняет усреднение концентраций изотопов по полиячейке

        Аргументы:
           lst : <lst<float>> - список концентраций изотопов в ячейках
        '''

    @abstractmethod
    def _after_concent(self, file_in):
        pass

    @abstractmethod
    def _before_concent(self, file_in):
        pass

    @abstractmethod
    def _concent(self, file_in):
        pass

    def _write_commands(self, file_in, commands):
        for cmd in commands:
            file_in.write(':%s\n' % cmd.name)
            file_in.write(' &vvod\n')
            if cmd.name == 'burn':
                file_in.write('  qv = {:.2f}\n'.format(cmd.data['qv']))
                file_in.write('  dtim = {:.2f}\n'.format(cmd.data['dtim']))
            elif cmd.name == 'macro':
                input_str = '  ET = '
                for pair in cmd.data['ET']:
                    input_str += '{:.2e},{:.2e}, '.format(pair[0], pair[1])
                file_in.write(input_str + '\n')
                input_str = ', '.join(map(str, cmd.data['NBV']))
                file_in.write('  NBV = %s,\n' % input_str)
            file_in.write(' &end\n')
        file_in.write(':stop\n')


class KorpCell(Cell):
    '''
    Ячейка корпусного реактора
    '''

    inp_file = 'korp.dat'
    out_file = 'korp.out'

    init_step = 5
    step = 20
    num_of_steps = 50

    def __init__(self, d, delta, r_ex, fuel, cool, temp):
        '''
        Задает основные параметры ячейки:
            d : float          - диаметр ТВЭЛа, см
            delta : float      - толщина оболочки ТВЭЛа, см
            r_ex : float       - радиус ячейки, см
            fuel : base.Matter - топливо
            cool : base.Matter - теплоноситель
            temp : Temp        - температуры топлива, конструкторских
                                 материалов и теплоносителя, K
        '''

        self.d = d
        self.delta = delta
        self.r_ex = r_ex
        self.fuel = fuel
        self.cool = cool
        self.temp = temp

    def camp_func(self, b, k_func):
        return k_func(b/3) + k_func(b/2) + k_func(b) - 3

    def find_r_opt(self, step_array):
        super().find_r_opt(step_array/2)

    def mean_func(self, lst):
        return lst[0]

    def _after_concent(self, file_in):
        file_in.write("  material(1) = 'chmc',\n")
        file_in.write(' &end\n')
        file_in.write('\n'.join(self.fuel.comp) + '\n')
        file_in.write('zr\n')
        file_in.write('\n'.join(self.cool.comp) + '\n')
        file_in.write('****\n')

    def _before_concent(self, file_in):
        file_in.write(':poly\n')
        file_in.write(' &vvod\n')
        file_in.write('  nsos = 1, 2, 3,\n')
        r_in, r = self.d/2 - self.delta, self.d/2
        file_in.write('  r = %s\n' % ('{:.3f}, '*3).format(r_in, r, self.r_ex))
        file_in.write('  t = %s\n' % ('{:.1f}, '*3).format(*self.temp[:3]))
        file_in.write('  troiz =\n')

    def _concent(self, file_in):
        for concent in self.fuel.comp.values():
            file_in.write('   %e, 0.0, 0.0,\n' % concent)
        file_in.write('   0.0, %e, 0.0,\n' % zr.comp['zr'])
        for concent in self.cool.comp.values():
            file_in.write('   0.0, 0.0, %e,\n' % concent)


class KanCell(Cell):
    '''
    Ячейка канального реактора
    '''

    inp_file = 'kan.dat'
    out_file = 'kan.out'

    init_step = 5
    step = 40
    num_of_steps = 50

    __FACTOR = 6  # количество ТВЭЛов в "рядах": n, 2n, 3n, где n <=> FACTOR

    __MATR_PATH = (path.dirname(path.abspath(__file__)) + sep +
                   '%dx%d matrices.txt')

    @property
    def mod(self):
        ''' Замедлитель '''

        return self.__mod

    @mod.setter
    def mod(self, value):
        self.__mod = deepcopy(value)
        self.__mod.add_mod_prop()

    @property
    def num_of_rods(self):
        ''' кол-во ТВЭЛов в ТВС '''

        return self.__num_of_rods

    @num_of_rods.setter
    def num_of_rods(self, value):
        self.__num_of_rods = value
        ratio = self.num_of_rods//self.__FACTOR
        self.__num_of_rows = int((-1 + sqrt(1 + 8*ratio))//2)

    @property
    def num_of_rows(self):
        ''' Количество рядов с твэлами '''

        return self.__num_of_rows

    def __init__(self, d, delta, num_of_rods, d_assly, delta_assly, r_ex,
                 num_of_rings, fuel, cool, mod, temp):
        '''
        Задает основные параметры ячейки:
            d : float           - диаметр ТВЭЛа, см
            delta : float       - толщина оболочки ТВЭЛа, см
            num_of_rods : int   - кол-во ТВЭЛов в ТВС
            d_assly : float     - диаметр ТВС, см
            delta_assly : float - толщина оболочки ТВС, см
            r_ex : float        - эквивалентный внешний радиус ячейки, см
            num_of_rings : int  - кол-во колец в разбиении замедлителя
            fuel : base.Matter  - топливо
            cool : base.Matter  - теплоноситель
            mod  : base.Matter  - замедлитель
            temp : Temp         - температуры топлива, конструкторских
                                  материалов, теплоносителя и замедлителя, K
        '''

        self.d = d
        self.delta = delta
        self.num_of_rods = num_of_rods
        self.d_assly = d_assly
        self.delta_assly = delta_assly
        self.r_ex = r_ex
        self.num_of_rings = num_of_rings
        self.fuel = fuel
        self.cool = cool
        self.mod = mod
        self.temp = temp

    def camp_func(self, b, k_func):
        return brentq(k_func, 0, b)/b - 1

    def find_r_opt(self, step_array):
        super().find_r_opt(step_array/pi**0.5)

    def mean_func(self, lst):
        result = sum(lst[i]*i for i in range(1, len(lst) - 1))
        return result / sum(i for i in range(1, len(lst) - 1))

    def _after_concent(self, file_in):
        input_str = ', '.join(map(str, range(1, self.num_of_rows + 3)))
        file_in.write('  ntcell = %s\n' % input_str)
        input_lst = [(i + 1)*self.__FACTOR for i in range(self.num_of_rows)]
        input_str = ', '.join(map(str, input_lst))
        file_in.write('  krat = 1, %s, 1,\n' % input_str)
        self.__write_matr(file_in)
        file_in.write("  material(1)='chmc',\n")
        file_in.write(' &end\n')
        file_in.write('\n'.join(self.fuel.comp) + '\n')
        file_in.write('zr\n')
        combo_comp = self.cool.comp.copy()
        combo_comp.update(self.mod.comp)
        file_in.write('\n'.join(combo_comp) + '\n')
        file_in.write('****\n')

    def _before_concent(self, file_in):
        file_in.write(':poly\n')
        file_in.write(' &vvod\n')
        file_in.write('  rcel(1, 1) = {:.3f},\n'.format(self.d/2))
        file_in.write('  ncelsos(1, 1) = 2,\n')
        s_assly = pi*(self.d_assly/2 - self.delta_assly)**2
        rod_r_ex = (s_assly/(self.num_of_rods + 1)/pi)**0.5
        self.__write_rods(file_in, rod_r_ex)
        self.__write_mod(file_in)
        input_str = ('{:.1f}, '*4).format(*self.temp)
        file_in.write('  t = %s\n' % input_str)
        file_in.write('  troiz =\n')

    def _concent(self, file_in):
        for izotop in self.fuel.comp:
            file_in.write('   %e, 0.0, 0.0, 0.0,\n' % self.fuel.comp[izotop])
        file_in.write('   0.0, %e, 0.0, 0.0,\n' % zr.comp['zr'])
        for izotop in self.cool.comp:
            input_str = '   0.0, 0.0, %e' % self.cool.comp[izotop]
            concent = self.mod.comp[izotop] if izotop in self.mod.comp else 0
            file_in.write(input_str + ', %e,\n' % concent)
        for izotop in self.mod.comp:
            if izotop not in self.cool.comp:
                concent = self.mod.comp[izotop]
                file_in.write('   0.0, 0.0, 0.0, %e,\n' % concent)

    def __write_matr(self, file_in):
        dim = self.__num_of_rows + 2
        matrices = open(self.__MATR_PATH % (dim, dim))
        for line in matrices:
            file_in.write(line)
        matrices.close()

    def __write_mod(self, file_in):
        num = self.__num_of_rows + 2
        input_str = '  rcel(1, %d) = ' % (num)
        r_array = linspace(self.d_assly/2, self.r_ex, self.num_of_rings + 1)
        input_str += ''.join(['{:.3f}, '.format(r) for r in r_array])
        r_inner = self.d_assly/2 - self.delta_assly
        input_str += 'rcin({}) = {:.3f},\n'.format(num, r_inner)
        file_in.write(input_str)
        input_str = '2, ' + '4, '*self.num_of_rings
        file_in.write('  ncelsos(1, %d) = %s\n' % (num, input_str))

    def __write_rods(self, file_in, rod_r_ex):
        for i in range(2, self.__num_of_rows + 2):
            r_in = self.d/2 - self.delta
            input_str = ('{:.3f}, '*3).format(r_in, self.d/2, rod_r_ex)
            file_in.write('  rcel(1, %d) = %s\n' % (i, input_str))
            file_in.write('  ncelsos(1, %d) = 1, 2, 3,\n' % i)
