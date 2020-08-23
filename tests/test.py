from os import sep, path
from importlib.util import module_from_spec, spec_from_file_location
from unittest import TestCase, main

FILE_PATH = path.dirname(path.abspath(__file__))

rbase_path = FILE_PATH + '{s}..{s}src{s}rbase.py'.format(s=sep)
spec = spec_from_file_location('rbase', rbase_path)
rbase = module_from_spec(spec)
spec.loader.exec_module(rbase)

wbase_path = FILE_PATH + '{s}..{s}src{s}wbase.py'.format(s=sep)
spec = spec_from_file_location('wbase', wbase_path)
wbase = module_from_spec(spec)
spec.loader.exec_module(wbase)


TEST_FILE = FILE_PATH + '{}test.out'.format(sep)
ANS_FILE = FILE_PATH + '{}test.ans'.format(sep)

class MatterTest(TestCase):

    def test_create_comp(self):
        spirit = rbase.Matter('C2H5OH', 0.789)
        spirit_comp = {'c': 2*0.010321, 'h': 6*0.010321, 'o': 0.010321}
        self.assertEqual(spirit_comp.keys(), spirit.comp.keys())
        for element, concent in spirit.comp.items():
            self.assertTrue(abs(concent - spirit_comp[element]) < 1e-05)

    def test_add_izotops(self):
        b_carbide = rbase.Matter('B4C', 2.52)
        b_carbide.add_izotops({'B': [('B10', 0.8), ('B11', 0.2)]})
        b_carbide_comp = {'b10': 4*0.027469*0.8,
                          'b11': 4*0.027469*0.2,
                          'c': 0.027469}
        for element, concent in b_carbide.comp.items():
            self.assertTrue(abs(concent - b_carbide_comp[element]) < 1e-05)

    def test_add_mod_prop(self):
        heavy_water = rbase.Matter('D2O', 1.1)
        heavy_water.add_mod_prop()
        heavy_water_comp = {'d': 2*0.033088, '*o*': 0.033088}
        for element, concent in heavy_water.comp.items():
            self.assertTrue(abs(concent - heavy_water_comp[element]) < 1e-05)

    def test_add_uranium(self):
        u_dioxide = rbase.Matter('UO2', 10.4)
        u_dioxide.add_uranium(0.0071)
        u_dioxide_comp = {'u235': 0.023196*0.0071,
                          'u238': 0.023196*0.9929,
                          'o': 2*0.023196}
        for element, concent in u_dioxide.comp.items():
            self.assertTrue(abs(concent - u_dioxide_comp[element]) < 1e-05)


class FileDataTest(TestCase):

    def test_find_coeff(self):
        coefficients = rbase.FileData.COEFF_DICT.keys()
        coeff_dict = {coeff: find_ans(coeff) for coeff in coefficients}
        data = rbase.FileData(TEST_FILE, coefficients=coefficients)
        data.find_coeff()
        for coeff in data.coeff_dict:
            self.assertEqual(data.coeff_dict[coeff], coeff_dict[coeff])

    def test_find_comp(self):
        data = rbase.FileData(TEST_FILE)
        mix = data.find_comp(10, 3, 3)
        self.assertEqual(mix.comp, {'*h*': 0.46760e-01,
                                    '*o*': 0.23380e-01})
        mix = data.find_comp(1, 4, 1)
        self.assertEqual(mix.comp, {'zr': 0.42910e-01})

    def test_find_concent(self):
        izotops = ['u235', 'u236']
        concent_dict = {izotop: find_ans(izotop) for izotop in izotops}
        data = rbase.FileData(TEST_FILE, izotops=izotops)
        data.find_concent(lambda lst: (lst[1] + lst[2]*2) / 3)
        for izotop in izotops:
            for i in range(len(data.concent_dict[izotop])):
                diff = data.concent_dict[izotop][i] - concent_dict[izotop][i]
                self.assertTrue(abs(diff) < 1e-07)
        norm = data.concent_dict['u235'][0]
        data.normalize({'u236': norm})
        for izotop in izotops:
            for i in range(len(data.concent_dict[izotop])):
                concent_dict[izotop][i] /= norm
                diff = data.concent_dict[izotop][i] - concent_dict[izotop][i]
                self.assertTrue(abs(diff) < 1e-7)

    def test_find_macro(self):
        constants = rbase.FileData.MACRO_DICT.keys()
        macro_dict = {macro: find_ans(macro) for macro in constants}
        data = rbase.FileData(TEST_FILE, constants=constants)
        data.find_macro(1)
        self.assertEqual(data.macro_dict, macro_dict)


def find_ans(str_quantity):
    ans_file = open(ANS_FILE)
    for line in ans_file:
        if str_quantity in line.split():
            ans_file.close()
            return eval(line.split(str_quantity)[-1])
    return None


if __name__ == '__main__':
    main()
