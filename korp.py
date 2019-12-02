from commands import write_commands
from constants import N_zr


def before_concent(file_in, d, delta, R):
    file_in.write(':poly\n')
    file_in.write(' &vvod\n')
    file_in.write(' nsos=1,2,3,\n')
    file_in.write(' r=' + ', '.join(map(str, [round(d/2 - delta, 5),
                                              round(d/2, 5), round(R, 5)])) +
                  ',\n')
    file_in.write(' t=1000.0, 600.0, 579.0,\n')
    file_in.write(' troiz=\n')


def concent(file_in, fuel_compos, coolant_compos):
    for izotop in fuel_compos:
        file_in.write(' ' + str(round(fuel_compos[izotop], 5)) +
                      ', 0.0, 0.0,\n')
    file_in.write(' 0.0, ' + str(round(N_zr, 5)) + ', 0.0,\n')
    for izotop in coolant_compos:
        file_in.write(' 0.0, 0.0, ' + str(round(coolant_compos[izotop], 5)) +
                      '\n')


def after_concent(file_in, fuel_compos, coolant_compos):
    file_in.write(" material(1)='chmc',\n")
    file_in.write('&end\n')
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
