import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from control.matlab import tf, step


df = pd.read_csv("PID_temp_filtered.csv")
setpoint = 85
start_temp = 55

time = df['time']
power = df['power ratio']
temperature = df['temperature_filtered']

#starting index from temperature is 55
start_idx = np.where(temperature >= start_temp)[0][0]
time_shifted = time[start_idx:] - time[start_idx]
temp_shifted = temperature[start_idx:]
power_shifted = power[start_idx:]

# PID
Kp = 50
Ki = 0.03
C = 4186
R = 0.44
#simulated transfer function
num = [R*Kp, R*Ki]  
den = [R*C, (1 + R*Kp), R*Ki]  
Gc = tf(num, den)


# step respose of simulated PID
y_norm, t_theory = step(Gc, T=time_shifted)

y_theory = y_norm * (setpoint - start_temp) + start_temp

# overshoot, settling time, risetime
overshoot = (temp_shifted.max() - setpoint)/(setpoint - start_temp)*100

t_rise_start = time_shifted[temp_shifted >= 0.1*(setpoint - start_temp) - start_temp].iloc[0]
t_rise_end   = time_shifted[temp_shifted >= start_temp + 0.9*(setpoint - start_temp)].iloc[0]
rise_time = t_rise_end - t_rise_start

tol = 0.05*(setpoint - start_temp)
settling_time = np.nan
for i in range(len(temp_shifted)):
    window = temp_shifted[i:]
    if np.all((window >= setpoint - tol) & (window <= setpoint + tol)):
        settling_time = time_shifted.iloc[i]
        break

# power ratio figure
plt.figure(figsize=(7,5))
plt.plot(time_shifted, power_shifted * 1500, color='orange', label='Heater Power')
plt.xlabel("Time (s)")
plt.ylabel("Power (W)")
plt.title("Heater Power (from 55°C)")
plt.grid()
plt.legend()

# temperature figure
plt.figure(figsize=(7,5))
plt.plot(time_shifted, temp_shifted, label='Measured Temperature', color='blue')
plt.plot(t_theory, y_theory, '--', label='Simulated PID Response', color='red')
plt.axhline(setpoint, color='black', linestyle='--', label='Setpoint')
plt.xlabel("Time (s)")
plt.ylabel("Temperature (°C)")
plt.title("Temperature (from 55°C)")
plt.grid()
plt.legend()

plt.text(0.5*max(time_shifted), setpoint-10,
         f"Overshoot: {overshoot:.2f}%\nRise Time: {rise_time:.2f}s\nSettling Time: {settling_time:.2f}s",
         bbox=dict(facecolor='white', alpha=0.7))

plt.show()
