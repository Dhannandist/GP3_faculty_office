
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

        # Update response status
        return self.receive_serial()

# Inheritance of SerialCom utilities
class Card(SerialCom):
    # Write into a card
    def write_card(self, data: str) -> str:
        write_result = self.send_serial("WRITE %s" %(data))
        if not write_result:
            print("Can't write into the card!")
            return None
        return write_result

    # Read card details
    def read_card_data(self) -> str:
        card_details = self.send_serial("READ")
        if not card_details:
            print("Can't get card's detail!")
            return None
        return card_details

    # Ping serial port to ensure serial communication is live
    def ping_serial(self, status_to_check: str="OK") -> str:
        if not self.is_initialized:
            print("not initialized")
            return False

        ping_result = self.send_serial("PING")
        if ping_result != status_to_check:
            print("not same")
            return False
        return ping_result

# Runs only when directly running this code standalone
if (__name__ == "__main__"):
    card = Card("COM5", 9600)
    print("Status: %s" %(card.ping_serial()))

    write_result = card.write_card("{'id': 0, 'room': 312}")
    if write_result == "SUCCESS":
        print("Successfully write card!")
        print(write_result)
        print("Details: %s" %(card.read_card_data()))