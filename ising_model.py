import numpy as np
from numpy.random import random, randint
import matplotlib.pyplot as plt

from utils_ising_model import are_nn, get_change_in_E, get_energy_of_spin, get_prob_of_flipping

# initialise constants
J, k_B = 1.0, 1.0
nstep = int(1e4)
output_filename = "spins.dat"
T = float(input("Temperature of the system: "))
lx = int(input("Length of the lattice's side: "))
ly = lx

# Generate NxN array of 1s and -1s
spin_array = np.array([1 if random() < 0.5 else -1 for _ in range(lx*ly)]).reshape((lx,ly))
print(spin_array)

fig = plt.figure()
im = plt.imshow(spin_array, animated=True)


def change_spin_glauber():
    itrial = randint(0,lx)
    jtrial = randint(0,ly)
    E = get_energy_of_spin(itrial, jtrial, spin_array, lx, ly, J)
    # flag corresponding to metropolis test: change spin if it
    # lowers the energy (ΔE < 0) or with prob exp(ΔE / (k_b)T)
    delta_E = get_change_in_E(E)
    metropolis_flag = random() <= get_prob_of_flipping(delta_E, k_B, T) 
    if E >= 0 or metropolis_flag:
        spin_array[itrial, jtrial] *= -1

def change_spin_kawasaki():
    # choose two spins randomly
    # TODO: change this code, looks awful
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
    E_spin1 = get_energy_of_spin(spin1[0], spin1[1], spin_array, lx, ly, J)
    E_spin2 = get_energy_of_spin(spin2[0], spin2[1], spin_array, lx, ly, J)
    delta_E = get_change_in_E(E_spin1) + get_change_in_E(E_spin2) 
    if (are_nn(spin1, spin2, lx, ly)):
        delta_E += 4
    
    metropolis_flag = random() <= get_prob_of_flipping(delta_E, k_B, T) 
    if delta_E <= 0 or metropolis_flag:
        spin_array[spin1[0], spin1[1]] *= -1
        spin_array[spin2[0], spin2[1]] *= -1

def sample_eq_state(dynamics):
    for epoch in range(nstep):
        for _ in range(lx):
            for _ in range(ly):
                # select spin randomly
                dynamics()
        
        if (epoch % 10 == 0): 
        # update measurements
        # dump output
            f = open(output_filename,'w')
            for i in range(lx):
                for j in range(ly):
                    f.write('%d %d %lf\n'%(i,j,spin_array[i,j]))
            f.close()
            # show animation
            plt.cla()
            im = plt.imshow(spin_array, animated=True, vmin=-1, vmax=1)
            plt.draw()
            plt.pause(0.0001)
    
def main():
    sample_eq_state(change_spin_glauber)
    # sample_eq_state(change_spin_kawasaki)

if __name__ == "__main__":
    main()
