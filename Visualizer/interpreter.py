from typing import Generator
import serial

def getpacket(data:bytes, packet_size:int)->list[bytes]:
    """Splits the incoming data into packets of a specified size."""
    raise NotImplementedError

class Transfer:
    """Handles data transfer over serial communication."""
    def __init__(self, port:str, baudrate:int=115200):
        self.channel = serial.Serial(port, baudrate)
    
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

    def getall(self)->bytes:
        """Reads all available data from the serial channel."""
        return self.channel.read_all()
    
    def recieve(self)->Generator[bytes]:
        """Recieves data continuously in an infinite loop."""
        while True:
            yield self.channel.readline()