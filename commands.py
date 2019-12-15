from collections import namedtuple


command = namedtuple('command', ['name', 'data'])


def write_commands(file_in, commands):
    ''' На основании переданного списка команд (commands) производит
        соответствующие записи во входной файл (file_in) '''

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

    for command in commands:
        locals()[command.name](file_in, command.data)
    file_in.write(':stop\n')
