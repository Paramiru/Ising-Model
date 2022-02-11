import numpy as np

def get_chi_error(mgns, num_spins, t=1.0, k_B=1.0, method='b', k=1000):
    if method != 'b' and method != 'j':
        raise ValueError("Method should be 'b' for Bootstrap or 'j' for jacknife")
    chis_resampled = []
    n = len(mgns)
    for i in range(k):
        if method == 'b':
            mgns_resampled = np.random.choice(mgns, size=n)
        else:
            mask = np.ones(mgns.shape, bool)
            mask[i] = False
            mgns_resampled = mgns[mask]
        chi = np.var(mgns_resampled) / (num_spins * k_B * t)
        chis_resampled.append(chi)
    chis_resampled = np.array(chis_resampled)
    result = np.std(chis_resampled)
    if (method == 'b'): return result
    else: return result * np.sqrt(len(chis_resampled))

def get_heat_error(energies, num_spins, t=1.0, k_B=1.0, method='b', k=1000):
    if method != 'b' and method != 'j':
        raise ValueError("Method should be 'b' for Bootstrap or 'j' for jacknife")
    heats_resampled = []
    n = len(energies)
    for i in range(k):
        if method == 'b':
            e_resampled = np.random.choice(energies, size=n)
        else:
            mask = np.ones(energies.shape, bool)
            mask[i] = False
            e_resampled = energies[mask]
        scaled_heat_cap = np.var(e_resampled) / (num_spins * k_B * t)
        heats_resampled.append(scaled_heat_cap)
    heats_resampled = np.array(heats_resampled)
    result = np.std(heats_resampled)
    if (method == 'b'): return result
    else: return result * np.sqrt(len(heats_resampled))