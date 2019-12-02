from numpy import pi, linspace


from constants import N_zr
from commands import write_commands


def before_concent(file_in, d, delta, R, D, Delta, num_of_fuel_rods,
                   num_of_mod_rings):
    def moderator(file_in, num, D, Delta, num_of_mod_rings):
        r_array = linspace(D/2, R, num_of_mod_rings+1)
        input_str = ' rcel(1,'+str(num)+')='
        for r in r_array:
            input_str += str(round(r, 5)) + ','
        input_str += 'rcin('+str(num)+')=' + str(round(D/2 - Delta, 5)) + ',\n'
        file_in.write(input_str)
        file_in.write(' ncelsos(1,'+str(num)+')=2,' +
                      '4,'*num_of_mod_rings + '\n')

    def fuel_rod(file_in, num, d, delta, r_ex):
        radii = ','.join(map(str, [round(d/2 - delta, 5), round(d/2, 5),
                                   round(r_ex, 5)]))
        file_in.write(' rcel(1,'+str(num)+')=' + radii + '\n')
        file_in.write(' ncelsos(1,'+str(num)+')=1,2,3,\n')

    file_in.write(':poly\n')
    file_in.write(' &vvod\n')
    file_in.write(' rcel(1,1)=' + str(round(d/2, 5)) + '\n')
    file_in.write(' ncelsos(1,1)=2,\n')
    S = pi*(D/2 - Delta)**2  # площадь ТВС
    S /= (num_of_fuel_rods + 1)  # площадь, принадлежащая одному стержню
    # S = pi*r_ex^2
    r_ex = (S / pi)**0.5
    fuel_rod(file_in, 2, d, delta, r_ex)
    fuel_rod(file_in, 3, d, delta, r_ex)
    if num_of_fuel_rods == 18:
        moderator(file_in, 4, D, Delta, num_of_mod_rings)
    elif num_of_fuel_rods == 36:
        fuel_rod(file_in, 4, d, delta, r_ex)
        moderator(file_in, 5, D, Delta, num_of_mod_rings)
    file_in.write(' t=1773.0, 543.0, 543.0, 873.0\n')
    file_in.write(' troiz=\n')


def concent(file_in, fuel_compos, coolant_compos, mod_compos):
    for izotop in fuel_compos:
        file_in.write(' ' + str(round(fuel_compos[izotop], 5)) +
                      ', 0.0, 0.0, 0.0,\n')
    file_in.write(' 0.0, ' + str(round(N_zr, 5)) + ', 0.0, 0.0,\n')
    for izotop in coolant_compos:
        input_str = ' 0.0, 0.0, ' + str(round(coolant_compos[izotop], 5))
        if izotop in mod_compos:
            input_str += ', ' + str(round(mod_compos[izotop], 5)) + ',\n'
        else:
            input_str += ', 0.0,\n'
        file_in.write(input_str)
    for izotop in mod_compos:
        if izotop not in coolant_compos:
            file_in.write(' 0.0, 0.0, 0.0, ' +
                          str(round(mod_compos[izotop], 5)) + ',\n')


def after_concent(file_in, fuel_compos, coolant_compos, mod_compos,
                  num_of_fuel_rods):
    def add_dicts(*dicts):
        result = {}
        for d in dicts:
            result.update(d)
        return result

    if num_of_fuel_rods == 18:
        file_in.write(' ntcell=1,2,3,4,\n')
        krat_str = ' krat=1.,6.,12.,1.,\n'
        matrices = open('4x4 matrices.txt')
    elif num_of_fuel_rods == 36:
        file_in.write(' ntcell=1,2,3,4,5,\n')
        krat_str = ' krat=1.,6.,12.,18.,1.,\n'
        matrices = open('5x5 matrices.txt')
    file_in.write(krat_str)
    for line in matrices:
        file_in.write(line)
    file_in.write(" material(1)='chmc',\n")
    file_in.write('&end\n')
    for izotop in fuel_compos:
        file_in.write(izotop + '\n')
    file_in.write('zr\n')
    compos = add_dicts(coolant_compos, mod_compos)
    for izotop in compos:
        input_str = '*' + izotop + '*' + '\n' if izotop != 'd' else 'd\n'
        file_in.write(input_str)
    file_in.write('****\n')


def create_file(file_in, d, delta, R, D, Delta, num_of_fuel_rods,
                num_of_mod_rings, fuel_compos, coolant_compos, mod_compos,
                commands):
    before_concent(file_in, d, delta, R, D, Delta, num_of_fuel_rods,
                   num_of_mod_rings)
    concent(file_in, fuel_compos, coolant_compos, mod_compos)
    after_concent(file_in, fuel_compos, coolant_compos, mod_compos,
                  num_of_fuel_rods)
    write_commands(file_in, commands)
    file_in.close()
