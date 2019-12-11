from collections import namedtuple


command = namedtuple('command', ['name', 'data'])


def write_commands(file_in, commands):
    for command in commands:
        globals()[command.name](file_in, command.data)
    file_in.write(':stop\n')


def burn(file_in, data):
    file_in.write(':burn\n')
    file_in.write(' &vvod qv=' + data['qv'] + ' dtim=' + data['dtim'] +
                  ' &end\n')


def corr(file_in, data):
    file_in.write(':corr\n')
    file_in.write(' &vvod &end\n')


def fier(file_in, data):
    file_in.write(':fier\n')
    file_in.write(' &vvod &end\n')


def macro(file_in, data):
    file_in.write(':macro\n')
    file_in.write(' &vvod\n')
    file_in.write('  ET = 10.5e+6,2.15, 2.15,0.,\n')
    file_in.write('  NBV = ' + data + '\n')
    file_in.write(' &end\n')


def camp(qv, time_step, num_of_step, initial_fier=True):
    camp = [command('burn', {'qv': str(qv), 'dtim': str(time_step)}),
            command('corr', None), command('fier', None)]*num_of_step
    if initial_fier:
        return [command('fier', None)] + camp
    return camp
