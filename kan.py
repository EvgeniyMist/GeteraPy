from subprocess import run
from numpy import pi, linspace, arange, argmax
from numpy import sqrt

from commands import write_commands, command
from constants import N_zr
import functions as func


class KanCell():

    def __init__(self, d, delta, fuel_rods_num, d_assly, delta_assly, r_out,
                 mod_rings_num, fuel_comp, cool_comp, mod_comp):
        self.d = d
        self.delta = delta
        self.fuel_rods_num = fuel_rods_num
        self.d_assly = d_assly
        self.delta_assly = delta_assly
        if r_out is None:
            self.find_r_opt()
        else:
            self.r_out = r_out
        self.mod_rings_num = mod_rings_num
        self.fuel_comp = fuel_comp
        self.cool_comp = cool_comp
        self.mod_comp = mod_comp

    def __write_mod(self, file_in, num):
        r_array = linspace(self.d_assly/2, self.r_out, self.mod_rings_num+1)
        input_str = '  rcel(1, %d) = ' % num
        for r in r_array:
            input_str += '{:.3f}, '.format(r)
        r_inner = self.d_assly/2 - self.delta_assly
        input_str += 'rcin(%d)' % num + ' = {:.3f},\n'.format(r_inner)
        file_in.write(input_str)
        file_in.write('  ncelsos(1, %d) = 2, ' % num +
                      '4, '*self.mod_rings_num + '\n')

    def __write_fuel_rod(self, file_in, num, r_ex):
        radii = ('{:.3f}, '*3).format(self.d/2 - self.delta, self.d/2, r_ex)
        file_in.write(('  rcel(1, %d) = ' + radii + '\n') % num)
        file_in.write('  ncelsos(1, %d) = 1, 2, 3,\n' % num)

    def __before_concent(self, file_in):
        file_in.write(':poly\n')
        file_in.write(' &vvod\n')
        file_in.write('  rcel(1, 1) = {:.3f},\n'.format(self.d/2))
        file_in.write('  ncelsos(1, 1) = 2,\n')
        S = pi*(self.d_assly/2 - self.delta_assly)**2  # площадь ТВС
        S /= (self.fuel_rods_num + 1)  # площадь, принадлежащая одному стержню
        r_ex = (S / pi)**0.5  # S = pi*r_ex^2
        num_of_rows = (-1 + sqrt(1+8*self.fuel_rods_num/6)) / 2  # кол-во рядов
        for i in range(int(num_of_rows)):
            self.__write_fuel_rod(file_in, i+2, r_ex)
        self.__write_mod(file_in, num_of_rows+2)
        #########################################################
        if 'c' in self.mod_comp:
            file_in.write('  t = 1773.0, 543.0, 543.0, 873.0,\n')
        else:
            file_in.write('  t = 1773.0, 543.0, 543.0, 323.0,\n')
        #########################################################
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
                file_in.write('   0.0, 0.0, 0.0, %e,\n' %
                              self.mod_comp[izotop])

    def __after_concent(self, file_in):
        if self.fuel_rods_num == 18:
            file_in.write('  ntcell = 1, 2, 3, 4,\n')
            krat_str = '  krat = 1, 6, 12, 1,\n'
            matrices = open('4x4 matrices.txt')
        elif self.fuel_rods_num == 36:
            file_in.write(' ntcell = 1, 2, 3, 4, 5,\n')
            krat_str = '  krat = 1, 6, 12, 18, 1,\n'
            matrices = open('5x5 matrices.txt')
        file_in.write(krat_str)
        for line in matrices:
            file_in.write(line)
        file_in.write("  material(1)='chmc',\n")
        file_in.write(' &end\n')
        for izotop in self.fuel_comp:
            file_in.write(izotop + '\n')
        file_in.write('zr\n')
        comp = {}
        comp.update(self.cool_comp)
        comp.update(self.mod_comp)
        for izotop in comp:
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

    def camp_kan(self, commands, result_dict):
        '''
        Рассчитывает кампанию и возвращает значения выгорания

        Аргументы:
            commands - необходимые для расчета команды
            result_dict - стандартный словарь для результатов
        '''

        def continuous_overloads(k_func, right_b, N=100):
            b_array = linspace(0, right_b, N)
            mean_k = mean([k_func(b) for b in b_array])
            return mean_k

        r_opt = self.find_r_opt_kan()
        file_in = open('kan.txt', 'w')
        self.create_file(file_in, commands)
        config('kan')
        run('getera.exe')
        func.find_coeff('kan.out', result_dict)
        func.find_concent('kan.out', result_dict, norm=False)
        # определяем максимальное выгорание исходя из непрерывых перегрузок
        burning_lst = func.find_burning('kan.out')
        k_func = lambda b: interp(b, burning_lst, result_dict['K'])
        result_func = lambda b: continuous_overloads(k_func, b) - 1
        end_burning = brentq(result_func, 0, max(burning_lst))
        func.clear_data(burning_lst, end_burning, result_dict)
        return burning_lst

    def find_r_opt(self, a_left=12, a_right=50, a_delta=1):
        '''
        Вычисляет оптимальный эквивалентный радиус

        Аргументы:
            r_left, r_right, r_delta - диапазон и шаг прогонки радиуса
        '''

        a_array = arange(a_left, a_right, a_delta)
        r_array = a_array / pi**0.5
        result_dict = {'K': []}
        func.config('kan')
        for r in r_array:
            file_in = open('kan.txt', 'w')
            self.r_out = r
            self.create_file(file_in, [command('fier', None)])
            run('getera.exe')
            func.find_coeff('kan.out', result_dict)
        return r_array[argmax(result_dict['K'])]
