import serial,time,os

ser = serial.Serial(
	port='/dev/ttyAMA0',
	baudrate=19200,
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS,
	timeout=1
	)

print("Serial is open: ")
print(bytes(ser.isOpen()))

print("Writing now...")


path = '/home/pi/Desktop/fingerprint3.jpg'
f = open(path, 'rb')
size = os.stat(path)
print("Total bytes of file:", size.st_size)
print(ser.inWaiting())
nextLine = f.read(19200)
while len(nextLine):
    ser.write(nextLine)
    nextLine = f.read(19200)


print(ser.inWaiting())    

print("Reading from serial port")
writeFile = open('/home/pi/Desktop/myFile.jpg', 'w+b')

def readBlockOfBytes(writeFile):
    nextLine = ser.readline(500)
    while len(nextLine):
        writeFile.write(nextLine)
        nextLine = ser.readline(500)

readBlockOfBytes(writeFile)
newSize = os.stat('/home/pi/Desktop/myFile')
print(newSize.st_size)


ser.close()
