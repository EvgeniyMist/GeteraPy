from numpy import pi, linspace


from constants import N_zr
from commands import write_commands


def before_concent(file_in, d, delta, R, D, Delta, num_of_fuel_rods,
                   num_of_mod_rings, mod):

    def moderator(file_in, num, D, Delta, n):
        r_array = linspace(D/2, R, n+1)
        input_str = '  rcel(1, %d) = ' % num
        for r in r_array:
            input_str += '{:.3f}, '.format(r)
        input_str += 'rcin({}) = {:.3f},\n'.format(num, D/2 - Delta)
        file_in.write(input_str)
        file_in.write(('  ncelsos(1, %d) = 2, ' + '4, '*n + '\n') % num)

    def fuel_rod(file_in, num, d, delta, r_ex):
        radii = ('{:.3f}, '*3).format(d/2 - delta, d/2, r_ex)
        file_in.write(('  rcel(1, %d) = ' + radii + '\n') % num)
        file_in.write('  ncelsos(1, %d) = 1, 2, 3,\n' % num)

    file_in.write(':poly\n')
    file_in.write(' &vvod\n')
    file_in.write('  rcel(1, 1) = {:.3f},\n'.format(d/2))
    file_in.write('  ncelsos(1, 1) = 2,\n')
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
    #########################################################
    if 'c' in mod:
        file_in.write('  t = 1773.0, 543.0, 543.0, 873.0,\n')
    else:
        file_in.write('  t = 1773.0, 543.0, 543.0, 323.0,\n')
    #########################################################
    file_in.write('  troiz =\n')


def concent(file_in, fuel_compos, coolant_compos, mod_compos):
    for izotop in fuel_compos:
        file_in.write('   %e, 0.0, 0.0, 0.0,\n' % fuel_compos[izotop])
    file_in.write('   0.0, %e, 0.0, 0.0,\n' % N_zr)
    for izotop in coolant_compos:
        input_str = '   0.0, 0.0, %e' % coolant_compos[izotop]
        if izotop in mod_compos:
            input_str += ', %e,\n' % mod_compos[izotop]
        else:
            input_str += ', 0.0,\n'
        file_in.write(input_str)
    for izotop in mod_compos:
        if izotop not in coolant_compos:
            file_in.write('   0.0, 0.0, 0.0, %e,\n' % mod_compos[izotop])


def after_concent(file_in, fuel_compos, coolant_compos, mod_compos,
                  num_of_fuel_rods):

    def add_dicts(*dicts):
        result = {}
        for d in dicts:
            result.update(d)
        return result

    if num_of_fuel_rods == 18:
        file_in.write('  ntcell = 1, 2, 3, 4,\n')
        krat_str = '  krat = 1, 6, 12, 1,\n'
        matrices = open('4x4 matrices.txt')
    elif num_of_fuel_rods == 36:
        file_in.write(' ntcell = 1, 2, 3, 4, 5,\n')
        krat_str = '  krat = 1, 6, 12, 18, 1,\n'
        matrices = open('5x5 matrices.txt')
    file_in.write(krat_str)
    for line in matrices:
        file_in.write(line)
    file_in.write("  material(1)='chmc',\n")
    file_in.write(' &end\n')
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
                   num_of_mod_rings, mod_compos.keys())
    concent(file_in, fuel_compos, coolant_compos, mod_compos)
    after_concent(file_in, fuel_compos, coolant_compos, mod_compos,
                  num_of_fuel_rods)
    write_commands(file_in, commands)
    file_in.close()
