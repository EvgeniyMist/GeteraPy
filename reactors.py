from subprocess import run
from collections import namedtuple
from numpy import pi, linspace, arange, argmax, mean, sqrt, interp
from scipy.optimize import brentq

from constants import N_zr
import functions as func


class KorpCell():
    '''
    Ячейка корпусного реактора
    '''

    def __init__(self, d, delta, r_ex, fuel_comp, cool_comp):
        '''
        Задает основные параметры ячейки:
            d - диаметр ТВЭЛа
            delta - толщина оболочки ТВЭЛа
            r_ex - радиус, ограничивающий принадлежащий ТВЭЛу теплоноситель
            fuel_comp - топливная композиция
            cool_comp - состав теплоносителя
        '''

        self.d = d
        self.delta = delta
        self.fuel_comp = fuel_comp
        self.cool_comp = cool_comp
        self.r_ex = r_ex
        # температуры материалов
        Temp = namedtuple('Temp', ('fuel', 'shell', 'cool'))
        self.temp = Temp(1000, 600, 579)
        # наименование вспомогательного файла
        self.file_name = 'korp'

    def __after_concent(self, file_in):
        file_in.write("  material(1) = 'chmc',\n")
        file_in.write(' &end\n')
        for izotop in self.fuel_comp:
            file_in.write('%s\n' % izotop)
        file_in.write('zr\n')
        for izotop in self.cool_comp:
            file_in.write('*%s*\n' % izotop if izotop != 'd' else 'd\n')
        file_in.write('****\n')

    def __before_concent(self, file_in):
        file_in.write(':poly\n')
        file_in.write(' &vvod\n')
        file_in.write('  nsos = 1, 2, 3,\n')
        r_in = self.d/2 - self.delta
        input_str = ('{:.3f}, '*3).format(r_in, self.d/2, self.r_ex)
        file_in.write('  r = %s\n' % input_str)
        input_str = ('{:.1f}, '*3).format(self.temp.fuel, self.temp.shell,
                                          self.temp.cool)
        file_in.write('  t = %s\n' % input_str)
        file_in.write('  troiz =\n')

    def __concent(self, file_in):
        for izotop in self.fuel_comp:
            file_in.write('   %e, 0.0, 0.0,\n' % self.fuel_comp[izotop])
        file_in.write('   0.0, %e, 0.0,\n' % N_zr)
        for izotop in self.cool_comp:
            file_in.write('   0.0, 0.0, %e,\n' % self.cool_comp[izotop])

    def create_file(self, file_in, commands):
        '''
        Создает входной файл для расчета

        Аргументы:
            file_in - файл записи
            commands - необходимые для расчета команды
        '''

        self.__before_concent(file_in)
        self.__concent(file_in)
        self.__after_concent(file_in)
        func.write_commands(file_in, commands)
        file_in.close()

    def find_r_opt(self, r_left=0.5, r_right=1.5, r_delta=0.025):
        '''
        Вычисляет оптимальный радиус ячейки

        Аргументы:
            r_left, r_right, r_delta - диапазон и шаг прогонки радиуса
        '''

        r_array = arange(r_left, r_right + r_delta, r_delta)
        result_dict = {'K': []}
        func.change_config(self.file_name)
        for r in r_array:
            file_in = open('%s.txt' % self.file_name, 'w')
            self.r_ex = r
            self.create_file(file_in, [func.Command('fier', None)])
            run('getera.exe', check=True)
            func.find_coeff('%s.out' % self.file_name, result_dict)
        self.r_ex = r_array[argmax(result_dict['K'])]

    def calcul_camp(self, commands, result_dict):
        '''
        Рассчитывает кампанию, производя записи значений коэффициента
        размножения нейтронов и концентраций заданных изотопов в переданную
        структуру данных и возвращает значения выгорания

        Аргументы:
            commands - необходимые для расчета команды
            result_dict - стандартный словарь для результатов
        '''

        file_in = open('%s.txt' % self.file_name, 'w')
        self.create_file(file_in, commands)
        func.change_config(self.file_name)
        run('getera.exe', check=True)
        func.find_coeff('%s.out' % self.file_name, result_dict)
        func.find_concent('%s.out' % self.file_name, result_dict, norm=False)
        burning_lst = func.find_burning('%s.out' % self.file_name)
        # определяем максимальное выгорание исходя из 3-ех перегрузок
        k_func = lambda b: interp(b, burning_lst, result_dict['K'])
        result_func = lambda b: k_func(b) + k_func(2*b) + k_func(3*b) - 3
        end_burning = 3*brentq(result_func, 1, burning_lst[-1])
        func.clear_data(burning_lst, end_burning, result_dict)
        return burning_lst


def continuous_overloads(k_func, right_b, points_num=100):
    '''
    По заданной зависимости K_eff от выгорания (k_func) возвращает его
    среднее значение на отрезке [0, right_b]

    Опциональные аргументы:
        points_num - кол-во точек для вычисления среднего значения
    '''

    b_array = linspace(0, right_b, points_num)
    mean_k = mean([k_func(b) for b in b_array])
    return mean_k


class KanCell():
    '''
    Ячейка канального реактора
    '''

    def __init__(self, d, delta, fuel_rods_num, d_assly, delta_assly, r_out,
                 mod_rings_num, fuel_comp, cool_comp, mod_comp):
        '''
        Задает основные параметры ячейки:
            d - диаметр ТВЭЛа
            delta - толщина оболочки ТВЭЛа
            fuel_rods_num - кол-во ТВЭЛов в ТВС
            d_assly - диаметр ТВС
            delta_assly - толщина оболочки ТВС
            r_out - эквивалентный внешний радиус ячейки
            mod_rings_num - кол-во колец, на которое разбивается замедлитель
            (необходимо для улучшения расчетной модели)
            fuel_comp - топливная композиция
            cool_comp - состав теплоносителя
            mod_comp - состав замедлителя
        '''

        self.d = d
        self.delta = delta
        self.fuel_rods_num = fuel_rods_num
        self.d_assly = d_assly
        self.delta_assly = delta_assly
        self.r_out = r_out
        self.mod_rings_num = mod_rings_num
        self.fuel_comp = fuel_comp
        self.cool_comp = cool_comp
        self.mod_comp = mod_comp
        # кол-во ТВЭЛов в одном ряду
        self.rods_in_row_num = 6
        # кол-во рядов ТВЭЛов
        ratio = self.fuel_rods_num/self.rods_in_row_num
        self.rows_num = int((-1 + sqrt(1 + 8*ratio))/2)
        # температуры материалов
        Temp = namedtuple('Temp', ('fuel', 'shell', 'cool', 'mod'))
        mod_temp = 873 if 'c' in mod_comp else 323
        self.temp = Temp(1773, 543, 543, mod_temp)
        # наименование вспомогательного файла
        self.file_name = 'kan'

    def __after_concent(self, file_in):
        input_str = '  ntcell ='
        for i in range(self.rows_num + 2):
            input_str += ' %d,' % (i + 1)
        file_in.write('%s\n' % input_str)
        input_str = '  krat = 1, '
        for i in range(self.rows_num):
            input_str += '%d, ' % ((i + 1)*self.rods_in_row_num)
        file_in.write('%s1,\n' % input_str)
        dim = self.rows_num + 2
        matrices = open('%dx%d matrices.txt' % (dim, dim))
        for line in matrices:
            file_in.write(line)
        file_in.write("  material(1)='chmc',\n")
        file_in.write(' &end\n')
        for izotop in self.fuel_comp:
            file_in.write('%s\n' % izotop)
        file_in.write('zr\n')
        comp = {}
        comp.update(self.cool_comp)
        comp.update(self.mod_comp)
        for izotop in comp:
            input_str = '*%s*\n' % izotop if izotop != 'd' else 'd\n'
            file_in.write(input_str)
        file_in.write('****\n')

    def __before_concent(self, file_in):
        file_in.write(':poly\n')
        file_in.write(' &vvod\n')
        file_in.write('  rcel(1, 1) = {:.3f},\n'.format(self.d/2))
        file_in.write('  ncelsos(1, 1) = 2,\n')
        s_assly = pi*(self.d_assly/2 - self.delta_assly)**2
        r_ex = (s_assly/(self.fuel_rods_num + 1)/pi)**0.5
        for i in range(self.rows_num):
            self.__write_fuel_rod(file_in, i + 2, r_ex)
        self.__write_mod(file_in, self.rows_num + 2)
        input_str = ('{:.1f}, '*4).format(self.temp.fuel, self.temp.shell,
                                          self.temp.cool, self.temp.mod)
        file_in.write('  t = %s\n' % input_str)
        file_in.write('  troiz =\n')

    def __concent(self, file_in):
        for izotop in self.fuel_comp:
            file_in.write('   %e, 0.0, 0.0, 0.0,\n' % self.fuel_comp[izotop])
        file_in.write('   0.0, %e, 0.0, 0.0,\n' % N_zr)
        for izotop in self.cool_comp:
            input_str = '   0.0, 0.0, %e' % self.cool_comp[izotop]
            if izotop in self.mod_comp:
                input_str += ', %e,\n' % self.mod_comp[izotop]
            else:
                input_str += ', 0.0,\n'
            file_in.write(input_str)
        for izotop in self.mod_comp:
            if izotop not in self.cool_comp:
                mod_concent = self.mod_comp[izotop]
                file_in.write('   0.0, 0.0, 0.0, %e,\n' % mod_concent)

    def __write_fuel_rod(self, file_in, num, r_ex):
        radii = ('{:.3f}, '*3).format(self.d/2 - self.delta, self.d/2, r_ex)
        file_in.write('  rcel(1, %d) = %s\n' % (num, radii))
        file_in.write('  ncelsos(1, %d) = 1, 2, 3,\n' % num)

    def __write_mod(self, file_in, num):
        r_array = linspace(self.d_assly/2, self.r_out, self.mod_rings_num + 1)
        input_str = '  rcel(1, %d) = ' % num
        for r in r_array:
            input_str += '{:.3f}, '.format(r)
        r_inner = self.d_assly/2 - self.delta_assly
        input_str += 'rcin({}) = {:.3f},\n'.format(num, r_inner)
        file_in.write(input_str)
        input_str = '2, ' + '4, '*self.mod_rings_num
        file_in.write('  ncelsos(1, %d) = %s\n' % (num, input_str))

    def create_file(self, file_in, commands):
        '''
        Создает входной файл для расчета

        Аргументы:
            file_in - файл записи
            commands - необходимые для расчета команды
        '''

        self.__before_concent(file_in)
        self.__concent(file_in)
        self.__after_concent(file_in)
        func.write_commands(file_in, commands)
        file_in.close()

    def find_r_opt(self, a_left=12, a_right=50, a_delta=1):
        '''
        Вычисляет оптимальный эквивалентный радиус

        Аргументы:
            r_left, r_right, r_delta - диапазон и шаг прогонки радиуса
        '''

        a_array = arange(a_left, a_right + a_delta, a_delta)
        r_array = a_array/pi**0.5
        result_dict = {'K': []}
        func.change_config(self.file_name)
        for r in r_array:
            file_in = open('%s.txt' % self.file_name, 'w')
            self.r_out = r
            self.create_file(file_in, [func.Command('fier', None)])
            run('getera.exe', check=True)
            func.find_coeff('%s.out' % self.file_name, result_dict)
        self.r_out = r_array[argmax(result_dict['K'])]

    def calcul_camp(self, commands, result_dict):
        '''
        Рассчитывает кампанию, производя записи значений коэффициента
        размножения нейтронов и концентраций заданных изотопов в переданную
        структуру данных и возвращает значения выгорания

        Аргументы:
            commands - необходимые для расчета команды
            result_dict - стандартный словарь для результатов
        '''

        file_in = open('%s.txt' % self.file_name, 'w')
        self.create_file(file_in, commands)
        func.change_config(self.file_name)
        run('getera.exe', check=True)
        func.find_coeff('%s.out' % self.file_name, result_dict)
        func.find_concent('%s.out' % self.file_name, result_dict, norm=False)
        # определяем максимальное выгорание исходя из непрерывых перегрузок
        burning_lst = func.find_burning('%s.out' % self.file_name)
        k_func = lambda b: interp(b, burning_lst, result_dict['K'])
        result_func = lambda b: continuous_overloads(k_func, b) - 1
        end_burning = brentq(result_func, 1, burning_lst[-1])
        func.clear_data(burning_lst, end_burning, result_dict)
        return burning_lst
