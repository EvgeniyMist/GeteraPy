def uo2_composition(x, gamma):
    if gamma is None:
        gamma = 10.97
    N0_uo2 = param_uo2*gamma
    return {'u238': N0_uo2*(1-x), 'u235': N0_uo2*x, 'o': N0_uo2*2}


def h2o_composition(gamma):
    if gamma is None:
        gamma = 1.0
    N_h2o = param_h2o*gamma
    return {'h': 2*N_h2o, 'o': N_h2o}


def d2o_composition(gamma):
    if gamma is None:
        gamma = 1.1
    N_d2o = param_d2o*gamma
    return {'d': 2*N_d2o, 'o': N_d2o}


def c_composition(gamma):
    return {'c': gamma*param_c}


param_uo2 = 0.002233 # яд/г / 10^24
param_h2o = 0.0334   # яд/г / 10^24
param_d2o = 0.0301   # яд/г / 10^24
param_c = 0.0502     # яд/г / 10^24


N_zr = 0.04291 # яд/cм^3 / 10^24


lambda_xe = 2.1*10**(-5)  # 1/c
lambda_i = 2.9*10**(-5)   # 1/c
sigma_a_xe = 3.5*10**6    # барн
sigma_a_xe *= 10**-24
