import serial
import serial.tools
import serial.tools.list_ports

class Arduino:
    def __init__(self, port, baudrate, timeout=1):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        # self.ser = serial.Serial(port, baudrate=baudrate, timeout=timeout)
        
        for port in serial.tools.list_ports.comports():
            if port.device == self.port:
                self.ser = serial.Serial(port.device, baudrate=self.baudrate, timeout=self.timeout)
                break

    def write(self, data):
        self.ser.write(data.encode())

    def read(self):
        return self.ser.readline().decode().strip()

    def read_bytes(self, size):
        return self.ser.read(size)

    def close(self):
        self.ser.close()

    def wait_for(self, message):
        while True:
            response = self.read()
            if message in response:
                return response
    
    def read_image(self, filename):
        # Read the image size
        image_size = int(self.read())
        print(f"Image size: {image_size} bytes")

        # Read the image data
        image_data = self.read_bytes(image_size)

        # Save the image data to a file
        with open(filename, 'wb') as f:
            f.write(image_data)
        print(f"Image saved to {filename}")

# Example usage
# if __name__ == "__main__":
#     arduino = Arduino(port='COM12', baudrate=115200, timeout=1)
#     arduino.read_image('received_image.jpg')
#     arduino.close()