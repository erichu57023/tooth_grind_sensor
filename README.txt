This code was originally written for use with the ME 178 Team 8 bruxism sensor.
It contains an Arduino sketch, ToothGrind.ino, to collect and digitize analog sensor data, and send it through a serial port.

SensorDataHandler.py contains methods to read serialized sensor data, and write it to a .csv file.
ProcessSensorData.py contains methods to analyze and display sensor data in real time.
Run both of these files from the command-line.
