"""
Created on Sat Jun 14 12:32:59 2025

@author: nampham
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

class MCS8ASpectrum:
    def __init__(self, filepath):
        self.filepath = filepath
        self.parameters = {}
        self.counts = []
        self.time_ns = []
        self._parse_file()

    def _parse_file(self):
        with open(self.filepath, 'r', encoding='utf-8', errors='ignore') as file:
            lines = file.readlines()
        try:
          with open(self.filepath, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        except FileNotFoundError:
          raise FileNotFoundError(f'Error: File {self.filepath} not found')
        except UnicodeDecodeError:
          raise UnicodeDecodeError(f'Error: Cannot decode {self.filepath} using UTF-8')
        except Exception as e:
          raise RuntimeError(f'Unexpected error while reading {self.filepath}: {e}')

        #Initialization
        data_start_index = None
        calfact_found = False

        #Obtain Parameters
        for i, line in enumerate(lines):
            stripped = line.strip()
            # Extract "key=value" lines
            if "=" in stripped and not stripped.startswith(";"):
                key, value = stripped.split("=", 1)
                key = key.strip()
                value = value.strip()
                #change to float
                try:
                    if '.' in value:
                        value = float(value)
                    else:
                        value = int(value)
                except ValueError:
                    pass  #if not the float then pass

                self.parameters[key] = value

        #Obtain Wave Data
        self.counts = [int(line.strip()) for line in lines[data_start_index:] if line.strip().isdigit()]
        self.time_ns = [i * self.parameters["calfact"] for i in range(len(self.counts))]

    def as_dataframe(self):
        return pd.DataFrame({
            "Time_ns": self.time_ns,
            "Counts": self.counts
        })
    
    def find_peaks(self):
        peaks, _ = find_peaks(self.as_dataframe()['Counts'], height=1000, distance=50)
        peak_counts = self.as_dataframe()['Counts'][peaks].tolist()
        peak_times = self.as_dataframe()['Time_ns'][peaks].tolist()
        time_diffs = np.concatenate([np.array([0]), np.diff(peak_times)])
        return pd.DataFrame({
            "Peak_counts": peak_counts,
            "Peak_times": peak_times,
            "Time_diff": time_diffs
        })

#File Name Definition
file_pass = ''
file_name = '20250612-testB4-2-NamPham.txt'
file_path_name = os.path.join(file_pass, file_name)

#Get data
spectrum = MCS8ASpectrum(file_path_name)
df_spectrum = spectrum.as_dataframe()
df_peaks = spectrum.find_peaks()


#Plot
#plt.rcParams['font.family'] = 'Times New Roman'

fig = plt.figure(figsize=(10, 4))
ax = fig.add_subplot(111)

ax.plot(df_spectrum["Time_ns"], df_spectrum["Counts"]/1e6, drawstyle='steps-mid')
ax.plot(df_peaks["Peak_times"], df_peaks["Peak_counts"]/1e6, "x", color='r')
ax.set_xlabel("Time (ns)")
ax.set_ylabel("Counts (million)")
ax.set_title("Time Spectrum from MCS8A with Peaks")
ax.text(2500, 2.05, f"Data obtained from: {file_name}", fontsize=5)
ax.grid(True)

plt.show()
