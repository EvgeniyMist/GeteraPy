from commands import write_commands
from constants import N_zr


def before_concent(file_in, d, delta, R):
    file_in.write(':poly\n')
    file_in.write(' &vvod\n')
    file_in.write('  nsos = 1, 2, 3,\n')
    file_in.write(('  r = ' + '{:.3f}, '*3 + '\n').format(d/2-delta, d/2, R))
    file_in.write('  t = 1000.0, 600.0, 579.0,\n')
    file_in.write('  troiz =\n')


def concent(file_in, fuel_compos, coolant_compos):
    for izotop in fuel_compos:
        file_in.write('   %e, 0.0, 0.0,\n' % fuel_compos[izotop])
    file_in.write('   0.0, %e, 0.0,\n' % N_zr)
    for izotop in coolant_compos:
        file_in.write('   0.0, 0.0, %e,\n' % coolant_compos[izotop])


def after_concent(file_in, fuel_compos, coolant_compos):
    file_in.write("  material(1) = 'chmc',\n")
    file_in.write(' &end\n')
    for izotop in fuel_compos:
        file_in.write(izotop + '\n')
    file_in.write('zr\n')
    for izotop in coolant_compos:
        input_str = '*' + izotop + '*' + '\n' if izotop != 'd' else 'd\n'
        file_in.write(input_str)
    file_in.write('****\n')


def create_file(file_in, d, delta, R, fuel_compos, coolant_compos, commands):
    before_concent(file_in, d, delta, R)
    concent(file_in, fuel_compos, coolant_compos)
    after_concent(file_in, fuel_compos, coolant_compos)
    write_commands(file_in, commands)
    file_in.close()
