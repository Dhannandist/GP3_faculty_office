
import serial
import time

class SerialCom:
    ser = None
    is_initialized = False

    # Initialization
    def __init__(self, *args, **kwargs):
        self.initialize(*args, **kwargs)
        
    # Initialize and open serial communication
    def initialize(self, COM_PORT: str="", BAUD_RATE: int=0):
        # Assign new values
        self.COM_PORT = COM_PORT
        self.BAUD_RATE = BAUD_RATE

        # Check and assign default values
        if self.COM_PORT == "":
            # COM port to use
            self.COM_PORT = "COM3"       ## Might be different on other computers/driver
        if self.BAUD_RATE == 0:
            self.BAUD_RATE = 9600        ## Adjust to the microcontroller's BAUD RATE

        # Create the instance of Serial
        self.ser = serial.Serial(self.COM_PORT, self.BAUD_RATE)

        # Ensure the device is ready
        if self.isReady():
            print("COM: %s\nBAUD_RATE: %s\n" %(self.COM_PORT, self.BAUD_RATE))
            self.is_initialized = True

    # Wait until device is ready
    def isReady(self) -> bool:
        print("Waiting till device is ready..")
        while True:
            read = self.ser.readline().decode(errors="ignore").strip()
            if read == "READY":
                print(read)
                return True
    # Close serial communication
    def close_serial(self):
        self.ser.close()
        self.serial_init = False

    # Receive data from COM
    def receive_serial(self, read_until_char: str="\n"):
        if not self.is_initialized:
            return False
        #output = self.ser.read_until(read_until_char).decode()
        output = self.ser.readline().decode(errors="ignore").strip()
        return output

    # Send data into serial
    def send_serial(self, output: str):
        if not self.is_initialized:
            return False
        # Ensure it has newline
        output += "\n"
        self.ser.write(output.encode())
        print("Sent")
        return True

    # Ping serial port to ensure serial communication is live
    def ping_serial(self, status_to_check: str="OK"):
        if not self.is_initialized:
            print("not initialized")
            return False

        if not self.send_serial("PING"):
            return False

        output = self.receive_serial()
        if output != status_to_check:
            print("not same")
            return False
        return output


# Runs only when directly running this code standalone
if (__name__ == "__main__"):
    com = SerialCom("COM5", 9600)
    print("Status: %s" %(com.ping_serial()))