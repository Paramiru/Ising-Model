import sys
import math
from random import random, randint
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# initialise constants
J, T, k_B = 1.0, 1.0, 10.0
nstep = int(1e4)

lx = int(input("Length of the lattice's side: "))
ly = lx

# Generate NxN array of 1s and -1s
spin_array = np.array([1 if random() < 0.5 else -1 for _ in range(lx*ly)]).reshape((lx,ly))
print(spin_array)

fig = plt.figure()
im = plt.imshow(spin_array, animated=True)

# note indexes in python are from 0 to n-1
def get_energy_of_spin(row: int, col: int, arr: np.array) -> int:
    el_1 = arr[(row+1) % lx, col] 
    el_2 = arr[row-1, col]
    el_3 = arr[row, (col+1) % ly] 
    el_4 = arr[row, col-1]
    return -J*arr[row,col]*(el_1 + el_2 + el_3 + el_4)

def get_prob_of_flipping(E: int):
    return np.exp(2*E / (k_B*T))

def try_change_spin():
    itrial = randint(0,lx-1)
    jtrial = randint(0,ly-1)
    E = get_energy_of_spin(itrial, jtrial, spin_array)
    # flag corresponding to metropolis test: change spin if it
    # lowers the energy (ΔE < 0) or with prob exp(ΔE / (k_b)T)
    print(E, get_prob_of_flipping(E))
    flipping_flag = random() <= get_prob_of_flipping(E) 
    if E >= 0 or flipping_flag :
        spin_array[itrial, jtrial] *= -1

def glauber():
# update loop here - for Glauber dynamics
    for epoch in range(nstep):
        for _ in range(lx):
            for _ in range(ly):
                # select spin randomly
                try_change_spin()
        
        if (epoch % 10 == 0): 
        # update measurements
        # dump output
            f = open('spins.dat','w')
            for i in range(lx):
                for j in range(ly):
                    f.write('%d %d %lf\n'%(i,j,spin_array[i,j]))
            f.close()
            # show animation
            plt.cla()
            im = plt.imshow(spin_array, animated=True)
            plt.draw()
            plt.pause(0.0001)

def kawasaki():
    pass

glauber()