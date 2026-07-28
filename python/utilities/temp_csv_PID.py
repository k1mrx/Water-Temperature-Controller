import time
import serial
import csv

PORT = '/dev/ttyUSB0' #enter your specefic port.
BAUD = 9600

ser = serial.Serial(PORT, BAUD, timeout=1)

time.sleep(2)  
ser.write(b'S') 
def PID_csv(ser = ser):
    with open('PID_temp.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['time', 'power ratio', 'temperature']) 

        #print("start...")

        while True:
            line = ser.readline().decode('utf-8', errors='ignore').strip()
            if not line:
                continue

            # for debug
            #print("DEBUG:", line)

            parts = line.split(',')
            if len(parts) == 3:
                time_s = float(parts[0]) / 1000.0
                power_ratio = float(parts[1])
                temperatue = float(parts[2])
                writer.writerow([time_s, power_ratio, temperatue])
                f.flush()
                print(parts)
            
