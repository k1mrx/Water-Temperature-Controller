import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.signal import butter, filtfilt

df = pd.read_csv('PID_temp.csv')
t = df['time']
T = df['temperature']
T = T - T.mean()

dt = t[1] - t[0]
fs = 1/dt
N = len(T)
fft_vals = np.fft.fft(T)
freqs = np.fft.fftfreq(N, dt)


positive_freqs = freqs[:N//2]
magnitude = np.abs(fft_vals[:N//2]) / N


plt.figure(figsize=(8,4))
plt.semilogy(positive_freqs, magnitude)
plt.xlabel("Frequency (Hz)")
plt.ylabel("Magnitude")
plt.title("Frequency Spectrum")
plt.grid(True)
plt.show()
