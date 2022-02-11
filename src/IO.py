import numpy as np

prefix = '../output_files/'

def write_data_mgn(ts, mgns, chis, chis_errors, filename):
    data = np.hstack((ts, mgns, chis, chis_errors))
    np.savetxt(prefix + filename + '_mgn,chi,chi_error.txt', data, delimiter=' ', fmt='%f')
    np.save(prefix + filename + '_mgn,chi,chi_error', data)

def write_data_energies(ts, energies, heats, heats_errors, filename):
    data = np.hstack((ts, energies, heats, heats_errors))
    np.savetxt(prefix + filename + '_energy,heat,heat_error.txt', data, delimiter=' ', fmt='%f')
    np.save(prefix + filename + '_energy,heat,heat_error.txt', data)