from subprocess import run
from numpy import interp, argmax, arange
from scipy.optimize import brentq

from commands import write_commands, command
from constants import N_zr
import functions as func


class KorpCell():

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
        if r_ex is None:
            self.find_r_opt()
        else:
            self.r_ex = r_ex

    def __before_concent(self, file_in):
        file_in.write(':poly\n')
        file_in.write(' &vvod\n')
        file_in.write('  nsos = 1, 2, 3,\n')
        file_in.write(('  r = '+'{:.3f}, '*3+'\n').format(self.d/2-self.delta,
                                                          self.d/2, self.r_ex))
        file_in.write('  t = 1000.0, 600.0, 579.0,\n')
        file_in.write('  troiz =\n')

    def __concent(self, file_in):
        for izotop in self.fuel_comp:
            file_in.write('   %e, 0.0, 0.0,\n' % self.fuel_comp[izotop])
        file_in.write('   0.0, %e, 0.0,\n' % N_zr)
        for izotop in self.cool_comp:
            file_in.write('   0.0, 0.0, %e,\n' % self.cool_comp[izotop])

    def __after_concent(self, file_in):
        file_in.write("  material(1) = 'chmc',\n")
        file_in.write(' &end\n')
        for izotop in self.fuel_comp:
            file_in.write(izotop + '\n')
        file_in.write('zr\n')
        for izotop in self.cool_comp:
            input_str = '*' + izotop + '*' + '\n' if izotop != 'd' else 'd\n'
            file_in.write(input_str)
        file_in.write('****\n')

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
        write_commands(file_in, commands)
        file_in.close()

    def calcul_camp(self, commands, result_dict):
        '''
        Рассчитывает кампанию и возвращает значения выгорания

        Аргументы:
            commands - необходимые для расчета команды
            result_dict - стандартный словарь для результатов
        '''

        file_in = open('korp.txt', 'w')
        self.create_file(file_in, commands)
        func.config('korp')
        func.run('getera.exe')
        func.find_coeff('korp.out', result_dict)
        func.find_concent('korp.out', result_dict, norm=False)
        burning_lst = func.find_burning('korp.out')
        # определяем максимальное выгорание исходя из 3-ех перегрузок
        k_func = lambda b: interp(b, burning_lst, result_dict['K'])
        result_func = lambda b: k_func(b) + k_func(2*b) + k_func(3*b) - 3
        end_burning = 3*brentq(result_func, 0, max(burning_lst))
        func.clear_data(burning_lst, end_burning, result_dict)
        return burning_lst

    def find_r_opt_korp(self, r_left=0.5, r_right=1.5, r_delta=0.025):
        '''
        Вычисляет оптимальный радиус ячейки

        Аргументы:
            r_left, r_right, r_delta - диапазон и шаг прогонки радиуса
        '''

        r_array = arange(r_left, r_right+r_delta, r_delta)
        result_dict = {'K': []}
        func.config('korp')
        for r in r_array:
            file_in = open('korp.txt', 'w')
            self.r_ex = r
            self.create_file(file_in, [command('fier', None)])
            run('getera.exe')
            func.find_coeff('korp.out', result_dict)
        self.r_ex = r_array[argmax(result_dict['K'])]
