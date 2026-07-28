import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

t = []
T = []

df = pd.read_csv('temperature_filtered.csv')
t = df['time'].values
T = df['temperature'].values
T_mid = T[1:]

dTdt = np.diff(T) / np.diff(t)
C = 4186 * 1.0
P = 1500
Tamb = 24.00

Rth = (T_mid - Tamb) / (P - C * dTdt)

mask = (T_mid > 55) & (T_mid < 90)
R_sel = Rth[mask]
T_sel = T_mid[mask]

#linear fitting for Rth
coef = np.polyfit(T_sel, R_sel, 1)
R0, R1 = coef[1], coef[0]
print(f"Rth(T) = {R0:.4f} + {R1:.6f} * T")


plt.figure()
plt.plot(t, T)
plt.xlabel('Time (s)')
plt.ylabel('Temperature (°C)')
plt.title('Water Temperature')
plt.grid(True)
    

plt.figure(figsize=(8,5))
plt.scatter(T_sel, R_sel, label='Rth ', color='blue')
plt.plot(T_sel, R0 + R1*T_sel, label= 'Linear fitting', color='red', linewidth=2)
plt.xlabel('Temperature (°C)')
plt.ylabel('Rth (°C/W)')
plt.title('Estimated Thermal Resistance')
plt.legend()
plt.grid(True)
plt.text(80, 10,
         f"Rth = {R0:.4f} + {R1:.6f}T",
         bbox=dict(facecolor='white', alpha=0.7))
plt.show()
