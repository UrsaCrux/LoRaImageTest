import serial
import serial.tools.list_ports

from typing import Generator

class Transfer:
    """Handles data transfer over serial communication."""
    def __init__(self, port:str, baudrate:int=115200, timeout:float|None = None, dtr:bool=False, rts:bool=False):
        try:
            # Channel setup
            self.channel = serial.Serial(port, baudrate, timeout=timeout)
            self.channel.dtr = dtr
            self.channel.rts = rts

            # Initial device info retrieval
            print(f"Connected to {port} at {baudrate} baud.")

        except serial.SerialException as serialerror:
            available_ports = serial.tools.list_ports.comports()
            raise ConnectionError(f"Could not open port {port}. Available ports: {[p.device for p in available_ports]}") from serialerror
        
        except Exception as e:
            raise e

    def getbyte(self)->bytes:
        """Reads a single byte from the serial channel."""
        return self.channel.read(1)
    
    def getbytes(self, n:int)->bytes:
        """Reads n bytes from the serial channel."""
        return self.channel.read(n)

    def getline(self)->bytes:
        """Reads a line from the serial channel."""
        return self.channel.readline()
    
    def getlines(self, n:int)->list[bytes]:
        """Reads n lines from the serial channel."""
        return [self.channel.readline() for _ in range(n)]

    def send(self, data:bytes)->int:
        """Sends data over the serial channel."""
        return self.channel.write(data)

    def receive(self)->Generator[bytes, None, None]:
        """Receives continuous data from the serial channel until timeout."""
        while line:=self.channel.readline():
            yield line
        print("Reception ended. No data received after timeout of", self.channel.timeout, "seconds.")