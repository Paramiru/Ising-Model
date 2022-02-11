from numpy.random import randint, random
from utils import get_energy_of_spin, get_change_in_E, get_prob_of_flipping, are_nn

def change_spin_glauber(spin_array, lx, ly, j, k_B, t):
    itrial = randint(0, lx)
    jtrial = randint(0, ly)
    E = get_energy_of_spin(itrial, jtrial, spin_array, lx, ly, j)
    delta_E = get_change_in_E(E)
    # flag corresponding to metropolis test: change spin if it
    # lowers the energy if (ΔE < 0) or with prob exp(ΔE / (k_b)T)
    metropolis_flag = random() <= get_prob_of_flipping(delta_E, k_B, t) 
    if delta_E < 0 or metropolis_flag:
        spin_array[itrial, jtrial] *= -1
        return delta_E 
    return 0

def change_spin_kawasaki(spin_array, lx, ly, j, k_B, t):
    # choose two spins randomly
    spins = randint(0, lx, size=(2,2))
    spin1 = spins[0]
    spin2 = spins[1]
    same_direction_flag = spin_array[spin1[0],spin1[1]] == spin_array[spin2[0], spin2[1]]

    while (same_direction_flag):
        spins = randint(0, lx, size=(2,2))
        spin1 = spins[0]
        spin2 = spins[1]
        same_direction_flag = spin_array[spin1[0],spin1[1]] == spin_array[spin2[0], spin2[1]]

    # Add (-1) because we are flipping the spins to compute the change in energy
    E_spin1 = get_energy_of_spin(spin1[0], spin1[1], spin_array, lx, ly, j)
    E_spin2 = get_energy_of_spin(spin2[0], spin2[1], spin_array, lx, ly, j)
    delta_E = get_change_in_E(E_spin1) + get_change_in_E(E_spin2) 
    if (are_nn(spin1, spin2, lx, ly)):
        delta_E += 4
    
    metropolis_flag = random() <= get_prob_of_flipping(delta_E, k_B, t) 
    if delta_E <= 0 or metropolis_flag:
        spin_array[spin1[0], spin1[1]] *= -1
        spin_array[spin2[0], spin2[1]] *= -1
        return delta_E
    return 0 