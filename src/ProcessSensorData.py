import serial
from serial.tools import list_ports
import csv
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import time
import SensorDataHandler as sensor

myPort = None

# Graph parameters
x_len = 300         # Number of points to display
y_range = [0, 1]  # Range of possible Y values to display
low, high = None, None

# Setup figure
fig = plt.figure()
ax1 = fig.add_subplot(1, 1, 1)
xs = list(np.linspace(-3, 0, x_len))
ys = [0] * x_len
ax1.set_ylim(y_range)

line, = ax1.plot(xs, ys, linewidth=4)
txt = ax1.text(0.05, 0.9, 'Activity profile: ', fontsize = 35, transform = ax1.transAxes)
plt.margins(x=0)

plt.title('Temporalis Muscle Activity Over Time')
plt.xlabel('Time (s)')
plt.ylabel('Normalized Muscle Activity (arbitrary units)')

# Activity types
classes = {
    0: 'NONE',
    1: 'CLENCHING',
    2: 'GRINDING',
    3: 'UNKNOWN'
}

def calibrate():
    # Identifies minimum and maximum signal strengths for normalization.
    lowBuffer = []
    print('    Please remain still (5 secs)...')
    timeout = time.time() + 5
    while time.time() < timeout:
        lowBuffer.append(sensor.readData())

    highBuffer = []
    print('    Please clench hard (3 secs)...')
    timeout = time.time() + 3
    while time.time() < timeout:
        highBuffer.append(sensor.readData())

    low = max([min(lowBuffer), 0])
    high = max(highBuffer) * 1.2
    return low, high

def animate(i):
    # Animation loop to update the figure.
    global ys, classes
    # Read a datapoint from the sensor
    data = (sensor.readData() - low) / (high - low)
    # Add y to list
    ys.append(data)
    # Remove oldest datapoint from list
    del ys[0]
    # Update line with new Y values
    line.set_ydata(ys)

    act = classifySignal()
    txt.set_text('Activity profile: ' + classes.get(act, 'UNKNOWN'))
    return line, txt

def classifySignal():
    # Classifies activity type based on signal characteristics. Modify if necessary.
    global ys
    recent = ys[-100:]
    # avg = np.nanmean(recent)
    # std = np.nanstd(recent)
    if np.mean(recent[-20]) < 0.1:
        return 0
    elif max(recent[-50:]) > 0.45:
        return 1
    # elif (avg > 0.1 or recent[-1] > 0.1) and std < 0.1:
    else:  
        return 2
    # else:
    #     return 3
    

if __name__ == '__main__':
    print('Searching for available COM ports...')
    activePort = sensor.scan()
    print('The first available port found is ' + activePort + '...')
    if sensor.connectToPort(activePort):
        print('Connected to ' + activePort + '!\n')
    else:
        print('Failed to connect to ' + activePort + '\n')
        exit()

    print('Calibrating...')
    low, high = calibrate()
    
    print('Calibration complete, opening graph...\n')
    ani = animation.FuncAnimation(fig, animate, interval = 10, blit = True)
    plt.show()
    print('Window closed, shutting down.')
    