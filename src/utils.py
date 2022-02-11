import numpy as np

# def get_total_energy(spin_array, lx: int, ly: int, J: int):
#     energy = 0
#     for row in range(lx):
#         for col in range(ly):
#             el_1 = spin_array[row-1, col]
#             el_2 = spin_array[row, (col+1) % ly] 
#             # energy += get_energy_of_spin(i, j, spin_array, lx, ly, J)
#             energy += -J * spin_array[row, col] * (el_1 + el_2)
#     return energy


def get_energy_of_spin(row: int, col: int, arr: np.array, lx: int, ly: int, J: float) -> int:
    el_1 = arr[(row+1) % lx, col] 
    el_2 = arr[row-1, col]
    el_3 = arr[row, (col+1) % ly] 
    el_4 = arr[row, col-1]
    return -J*arr[row,col]*(el_1 + el_2 + el_3 + el_4)

def get_change_in_E(E: int) -> int:
    return -2*E

def get_prob_of_flipping(delta_E: int, k_B: float, T: float) -> float:
    return np.exp(-delta_E / (k_B*T))

def are_nn(spin1: int, spin2: int, lx: int, ly: int) -> bool:
    return ((spin1[0] + 1) % lx == spin2[0] and spin1[1] == spin2[1] or
        (spin1[0] - 1) % lx == spin2[0] and spin1[1] == spin2[1] or
        spin1[0] == spin2[0] and (spin1[1] + 1) % ly == spin2[1] or
        spin1[0] == spin2[0] and (spin1[1] - 1) % ly == spin2[1]
        )