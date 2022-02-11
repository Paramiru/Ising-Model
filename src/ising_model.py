import numpy as np
from numpy.random import random
import matplotlib.pyplot as plt

from dynamics import change_spin_glauber, change_spin_kawasaki
from IO import write_data_energies, write_data_mgn
from resampling import get_chi_error, get_heat_error

class IsingModel:
    def __init__(self, nstep=int(1e4), filename='spins_dat'):
        self.j, self.k_B, self.t = 1.0, 1.0, 1.0
        self.nstep = nstep
        self.filename = filename
        self.lx = int(input("Length of the lattice's side: "))
        self.ly = self.lx
        self.N = self.lx * self.ly
        self.total_e = 0
        self.spin_array = np.array([1 if random() < 0.5 else -1 \
            for _ in range(self.N)]).reshape((self.lx, self.ly))

    def get_total_energy(self):
        nn = np.roll(self.spin_array, 1, axis=0) + np.roll(self.spin_array, 1, axis=1)
        energy = -np.sum(self.spin_array * nn)
        return energy
        
    def plot_equilibrium_state(self):
        dynamics_chosen = input("Input g for Glauber or k for Kawasaki dynamics: ").lower()
        if dynamics_chosen == 'g':
            dynamics = change_spin_glauber
        elif dynamics_chosen == 'k':
            dynamics = change_spin_kawasaki
        else:
            raise ValueError('Invalid dynamics provided. Input ' + 
                '\'g\' for Glauber or \'k\' for Kawasaki')

        self.t = float(input("Temperature of the system: ")) 
        plt.figure()
        plt.imshow(self.spin_array, animated=True)

        for epoch in range(self.nstep):
            for _ in range(self.N):
                    # select spin randomly
                    dynamics(self.spin_array, self.lx, self.ly, self.j, self.k_B, self.t)
            if (epoch % 10 == 0): 
                # update measurements
                # dump output
                f = open(self.filename,'w')
                for i in range(self.lx):
                    for j in range(self.ly):
                        f.write('%d %d %lf\n'%(i, j, self.spin_array[i,j]))
                f.close()
                # show animation
                plt.cla()
                plt.imshow(self.spin_array, animated=True, vmin=-1, vmax=1)
                plt.draw()
                plt.pause(0.0001)

    def __get_mgn_and_energy_for_t(self, t: int, dynamics):
        mgns = []
        energies = []
        self.total_e = self.get_total_energy()
        print(f"System starts temperature {t:.1f} with total energy: {self.total_e}")
        print(f"System has magnetisation { np.sum(self.spin_array)}")
        for epoch in range(self.nstep):
            for _ in range(self.N):
                # select spin randomly
                dynamics(self.spin_array, self.lx, self.ly, self.j, self.k_B, t)
            if (epoch >= 100):
                # wait 100 epochs to lose information about initial state
                if (epoch % 10 == 0):
                    # take measurements every 10 sweeps bc of autocorrelation time
                    mgn = np.sum(self.spin_array)
                    mgns.append(mgn)
                    self.total_e = self.get_total_energy()
                    print(f"Epoch {epoch}, total energy measured {self.total_e}")
                    energies.append(self.total_e)

        mgns = np.array(mgns)
        # want absolute value for magnetisation
        avg_abs_mgn = np.mean(np.abs(mgns))
        # Chi = (<M**2> - <M>**2) / (N * k_B * t)
        # chi is not calculated with abs value of magnetisation. Use mgns array
        chi = np.var(mgns) / (self.k_B * t * self.N)
        chi_error = get_chi_error(mgns, self.N, t=t)

        energies = np.array(energies)
        avg_total_e = np.mean(energies)
        # Cv / N = (<E**2> - <E>**2) / (N * k_B * t**2)
        scaled_heat_cap = np.var(energies) / (self.N * self.k_B * t**2)
        scaled_heat_cap_error = get_heat_error(energies, self.N, t=t)

        return avg_abs_mgn, chi, chi_error, avg_total_e, scaled_heat_cap, scaled_heat_cap_error
                
    def get_magnetisation_and_energy_data(self, ts, dynamics=change_spin_glauber):
        # initialise state for Glauber dynamics
        if (dynamics == change_spin_glauber):
            self.spin_array = np.ones((self.lx, self.lx))
            print("Using Glauber Dynamics")
            print(f"Initialise spin array to ground state: \n{self.spin_array}\n")
        elif (dynamics == change_spin_kawasaki):
            arr = np.ones((int(self.lx/2), self.lx))
            if (self.lx % 2 == 1):
                middle_row = np.hstack(( np.ones(int(self.lx/2)), np.ones(int(self.lx/2) + 1) * -1 ))
                self.spin_array = np.vstack((arr, middle_row, (-1) * arr))
            else:
                self.spin_array = np.vstack((arr, (-1) * arr))
            print("Using Kawasaki Dynamics")
            print(f"Initialise spin array to ground state: \n{self.spin_array}")
        else:
            raise ValueError('Algorithm provided is neither Glauber nor Kawasaki')
        # empty lists to store results for each temperature
        mgns, chis, chis_errors, energies, heats, heats_errors = [], [], [], [], [], []

        for t in ts:
            print(f"Modelling temperature {t:.1f}")
            print(f"Current spin array is:\n{self.spin_array}")

            avg_abs_mgn, chi, chi_error, avg_total_e, sc_heat_cap, \
                sc_heat_error = self.__get_mgn_and_energy_for_t(t, dynamics)
            mgns.append(avg_abs_mgn)
            chis.append(chi)
            chis_errors.append(chi_error)
            energies.append(avg_total_e)
            heats.append(sc_heat_cap)
            heats_errors.append(sc_heat_error)

            print(f"--> <|M|> = {avg_abs_mgn}")
            print(f"-->   ꭓ = {chi}")
            print(f"-->   σ_ꭓ = {chi_error}")
            print(f"-->  <E> = {avg_total_e}")
            print(f"-->   C = {sc_heat_cap}")
            print(f"-->   σ_c = {sc_heat_error}")

        ts = ts[:, None]
        mgns = np.array(mgns)[:, None]
        chis = np.array(chis)[:, None]
        chis_errors = np.array(chis_errors)[:, None]
        energies = np.array(energies)[:, None]
        heats = np.array(heats)[:, None]
        heats_errors = np.array(heats_errors)[:, None]

        write_data_energies(ts, energies, heats, heats_errors, self.filename)
        # Do not write mgn / chi values for Kawasaki
        if dynamics == change_spin_glauber:
            write_data_mgn(ts, mgns, chis, chis_errors, self.filename)
 
def main():
    isingModel = IsingModel(filename='example')
    isingModel.plot_equilibrium_state()

if __name__ == "__main__":
    main()