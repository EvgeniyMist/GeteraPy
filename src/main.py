from os import linesep
from sys import exit as sys_exit
from inspect import getfullargspec
import pydoc

from labs import lab5, lab6, lab7, lab8


AVAILABLE_LABS = (5, 6, 7, 8)

if __name__=='__main__':
    labno = int(input('Введите номер лабораторной: '))
    if labno not in AVAILABLE_LABS:
        sys_exit('К сожалению, данная лабораторная недоступна')
    lab_func = globals()['lab%d' % labno]
    print('Введите величины в соответствии со следующей docstring' + linesep)
    pydoc.help(lab_func)
    args = []
    for arg_name in getfullargspec(lab_func)[0]:
        args.append(input('Введите %s: ' % arg_name))
        try:
            args[-1] = float(args[-1])
        except ValueError:
            continue
    lab_func(*args)
