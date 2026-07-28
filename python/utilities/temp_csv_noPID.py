import csv
import serial
import time

ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
time.sleep(2)  
ser.write(b'S') 
with open('temperature.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['time', 'temperature'])  # header

    while True:
        line = ser.readline().decode('utf-8', errors='ignore').strip()
        if not line:
            continue

        # for debug
        #print("DEBUG:", line)

        parts = line.split(',')
        if len(parts) == 2:
            time_s = float(parts[0]) / 1000.0
            temperatue = float(parts[1])
            writer.writerow([time_s, temperatue])
            f.flush()
            print(parts)
print('CSV file created')                