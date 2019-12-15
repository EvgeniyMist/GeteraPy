import constants as const
import functions as func


def hw4(d, delta, x_u, x_pu, gamma_fuel, gamma_cool_korp, qv_korp,
        D, Delta, num_of_fuel_rods, cool, mod, gamma_cool_kan,
        gamma_mod, num_of_mod_rings, qv_kan):

    key = ' '
    # рассчитываем кампанию корпусного реактора
    fuel_compos_korp = const.uo2_composition(x_u, x_pu, gamma_fuel)
    cool_compos_korp = getattr(const, 'h2o_composition')(gamma_cool_korp)
    korp_dict = {key: {'K': [], 'u235': [const.param_uo2*gamma_fuel*x_u],
                       'pu39': [const.param_uo2*gamma_fuel*x_pu],
                       'pu40': [0], 'pu41': [0], 'pu42': [0], 'pu38': [0]}}
    burning_lst_korp = func.camp_korp(d, delta, fuel_compos_korp,
                                      cool_compos_korp,
                                      func.camp(qv_korp, 50, 25),
                                      korp_dict[key])
    # рассчитываем кампанию канального реактора
    fuel_compos_kan = func.find_compos('lab5.out', len(burning_lst_korp)-1, 1)
    fuel_compos_kan = {i: c for i, c in fuel_compos_kan.items()
                       if i != 'xe35' and c != 0}
    cool_compos_kan = getattr(const, cool + '_composition')(gamma_cool_kan)
    mod_compos = getattr(const, mod + '_composition')(gamma_mod)
    kan_dict = {key: {'K': [], 'u235': [], 'pu39': [], 'pu40': [], 'pu41': [],
                      'pu42': [], 'pu38': []}}
    for var in kan_dict[key]:
        if var in fuel_compos_kan:
            kan_dict[key][var].append(fuel_compos_kan[var])
    burning_lst_kan = func.camp_kan(d, delta, D, Delta, num_of_fuel_rods,
                                    fuel_compos_kan, cool_compos_kan,
                                    mod_compos, num_of_mod_rings,
                                    func.camp(qv_kan, 5, 25), kan_dict[key])
    # вывод результатов
    result_dict = korp_dict.copy()
    for var in result_dict[key]:
        result_dict[key][var] += kan_dict[key][var]
    burning = burning_lst_korp + list(map(lambda b: b + burning_lst_korp[-1],
                                          burning_lst_kan))
    func.normalize(result_dict[key])
    func.draw('HW4', burning, result_dict, r'Выгорание, $\frac{МВт\ сут}{кг}$')
