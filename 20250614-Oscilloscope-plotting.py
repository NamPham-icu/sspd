"""
Created on Sat Jun 14 14:29:21 2025

@author: nampham
"""

import os
import numpy as np
from scipy import fftpack
from scipy.optimize import curve_fit
from matplotlib import pyplot as plt

file_path = ''
file_name = '20250610-pulse-amp-chan1-NamPham.csv'
file_path_name = os.os.path.join(file_path, file_name)
delimiter = ','

try:
  with open(file_path, 'r') as file:
    data = np.loadtxt(file_path, delimiter=delimiter, skiprows=0) # loading the data
    print(f'File loaded successfully!')
    print(f'Data: \n{data}\ndata type = {type(data)} \ndata.shape = {data.shape}')
except FileNotFoundError:
  print(f'Error: File {file_path} not found')
except ValueError:
  print(f'Error: Format of the file {file_path} is not compatible')
except Exception as e:
  print(f'An error occurred: {e}')

# --- Time axis setting ---
dt = float(input("Time resolution (μs)="))
time = np.array([0 + dt*i for i in range(len(data))])

# --- Plotting Raw Graph ----
#plt.rcParams['font.family'] = 'Times New Roman'
fig = plt.figure(figsize=(10,4))
ax = fig.add_subplot(111)

ax.plot(time, data)
ax.set_xlabel("Time (μs)")
ax.set_ylabel("Voltage (V)")
ax.set_title("Pulse Signal")
ax.grid()
#ax.text(<x-coordinate>, <y-coordinate>, f"Data obtained from: {file_name}", fontsize=5)
plt.plot()

"""
# --- Extracting the analysis interval ---
start_idx = 24
end_idx = 179
time_seg = time[start_idx:end_idx + 1] - time[start_idx]
data_seg = data[start_idx:end_idx + 1]

# --- Defining damped oscillation model function ---
def damped(t, A, alpha, omega, phi, C):
    return A * np.exp(-alpha * t) * np.cos(omega * t + phi) + C

# --- Guessing Initial Values ---
C0 = np.mean(data_seg[-30:])                 # consider the average of the last 30 points as offset
A0 = data_seg[0] - C0                        # initial amplitude
Y = np.fft.rfft(data_seg - C0)
freqs = np.fft.rfftfreq(len(data_seg), dt)
freq_guess = freqs[np.argmax(np.abs(Y[1:])) + 1] if len(Y) > 1 else 1e7
omega0 = 2 * np.pi * freq_guess

p0 = [A0, 1e7, omega0, 0.0, C0]  # [A, α, ω, φ, C]

# --- Nonlinear least squares fitting ---
popt, pcov = curve_fit(damped, time_seg, data_seg, p0=p0, maxfev=20000)
A_fit, alpha_fit, omega_fit, phi_fit, C_fit = popt
tau_fit = 1 / alpha_fit
fd_fit = omega_fit / (2 * np.pi)
zeta_fit = alpha_fit / np.sqrt(alpha_fit**2 + omega_fit**2)

# --- Fitting error evaluation ---
residuals = time_seg - damped(time_seg, *popt)
R2 = 1 - np.sum(residuals**2) / np.sum((data_seg - np.mean(data_seg))**2)

# --- Visulalization ---
plt.figure(figsize=(8, 4))
plt.plot(time_seg * 1e9, data_seg, label="data")
plt.plot(time_seg * 1e9, damped(time_seg, *popt), label="fit", linewidth=2)
plt.xlabel("Time (ns)")
plt.ylabel("Amplitude")
plt.title("Damped Oscillation Fit (25–180th samples)")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

# --- Estimated Parameters ---
print("Fitted Parameters:")
print(f"A     = {A_fit:.6g}")
print(f"alpha = {alpha_fit:.6g}  [1/s]")
print(f"tau   = {tau_fit:.6g}    [s]")
print(f"omega = {omega_fit:.6g}  [rad/s]")
print(f"fd    = {fd_fit:.6g}     [Hz]")
print(f"phi   = {phi_fit:.6g}    [rad]")
print(f"C     = {C_fit:.6g}")
print(f"zeta  = {zeta_fit:.6g}")
print(f"R^2   = {R2:.6f}")
