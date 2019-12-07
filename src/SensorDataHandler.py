import serial
import csv
from serial.tools import list_ports

myPort = None

def scan():
    # Scans for available COM ports, returns the first open one.
    PortList = []
    while not PortList:
        PortList = list(list_ports.comports())

    activePort = PortList[0].device
    return activePort

def connectToPort(activePort):
    # Attempts to connect to the port provided.
    global myPort
    try:
        myPort = serial.Serial(activePort, 9600)
        if not myPort.is_open:
            print('Error: ' + activePort + ' is closed')
            return False
        return True
    except Exception as e:
        print(e)
        return False

def readData():
    # Reads data from the serial port.
    try:
        global myPort
        ser_read = myPort.readline()
        decode_read = float(ser_read)
        return decode_read
    except KeyboardInterrupt:
        raise
    except:
        return readData()

def writeToFile(filename):
    # Writes serial data to a csv file.
    global myPort
    myPort.reset_input_buffer()
    while True:
        try:
            decode_read = str(readData())
            print(decode_read)
            with open(filename + '.csv', 'a', newline='') as file:
                writer = csv.writer(file, delimiter = ",")
                writer.writerow([decode_read])
        except KeyboardInterrupt:
            raise
        except:
            continue

if __name__ == '__main__':
    print('Searching for available COM ports...')
    activePort = scan()
    print('The first available port found is ' + activePort + '...')
    if connectToPort(activePort):
        print('Connected to ' + activePort + '!\n')
    else:
        print('Failed to connect to ' + activePort + '\n')
        exit()

    filename = input('Please provide a filename to save data to: ')
    try:
        writeToFile(filename)
    except KeyboardInterrupt:
        print('Closing writer, flushing...')
        myPort.flush()
        print('Program closed successfully')