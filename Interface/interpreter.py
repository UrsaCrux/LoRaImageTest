import serial
import serial.tools.list_ports

from typing import Generator

class Packet:
    """Handles packet data using the PHUC Protocol.
    
    Header
    ------
    1 byte: Magic Num ()
    1 byte: Packet type

    Body
    ----
    4 bytes: timestamp
    Up to 16 bytes: data

    Tail
    ----
    2 bytes: CRC data
    
    Packet size (8 -> 24) inclusive

    Parameters
    ----------

    Methods
    -------
    """
    def __init__(self):
        self.data = None
        self.type = None
        self.crcpass = False
        self.timestamp = None
        pass

    def __str__(self):
        return f"""Packet object with:
        Packet type: {self.type}
        """

class Transfer:
    """
    Handles data transfer over serial communication.

    Parameters
    ----------
    port : str
        Serial port name (e.g., 'COM3', '/dev/ttyUSB0').
    baudrate : int, optional
        Communication speed in baud. Default is 115200.
    timeout : float or None, optional
        Read timeout in seconds. None means blocking mode. Default is None.
    dtr : bool, optional
        Data Terminal Ready line state. Default is False.
    rts : bool, optional
        Request To Send line state. Default is False.
    """

    def __init__(self, port:str, baudrate:int=115200, timeout:float|None = None, dtr:bool=False, rts:bool=False):
        try:
            # Channel setup
            self.channel = serial.Serial(port, baudrate, timeout=timeout)
            self.dtr = dtr
            self.rts = rts
            self.channel.dtr = dtr
            self.channel.rts = rts

            # Initial device info retrieval
            print(f"Connected to {port} at {baudrate} baud.")

        except serial.SerialException as serialerror:
            available_ports = serial.tools.list_ports.comports()
            raise ConnectionError(f"Could not open port {port}. Available ports: {[p.device for p in available_ports]}") from serialerror
        
        except Exception as e:
            raise e

    def getbyte(self) -> bytes:
        """
        Reads a single byte from the serial channel.

        Returns
        -------
        bytes
            The byte read, or b'' if timeout occurs.
        """
        return self.channel.read(1)

    def getbytes(self, n: int) -> bytes:
        """
        Reads n bytes from the serial channel.

        Parameters
        ----------
        n : int
            Number of bytes to read.

        Returns
        -------
        bytes
            Bytes read, or fewer if timeout occurs.
        """
        return self.channel.read(n)

    def getline(self) -> bytes:
        """
        Reads a line from the serial channel (until newline or timeout).

        Returns
        -------
        bytes
            The line read, including the newline character, or b'' if timeout occurs.
        """
        return self.channel.readline()

    def getlines(self, n: int) -> list[bytes]:
        """
        Reads n lines from the serial channel.

        Parameters
        ----------
        n : int
            Number of lines to read.

        Returns
        -------
        list of bytes
            List of lines read (each as bytes).
        """
        return [self.channel.readline() for _ in range(n)]

    def send(self, data: bytes) -> int:
        """
        Sends data over the serial channel.

        Parameters
        ----------
        data : bytes
            Data to send.

        Returns
        -------
        int
            Number of bytes written.
        """
        return self.channel.write(data)

    def receive(self) -> Generator[bytes, None, None]:
        """
        Receives continuous data from the serial channel until timeout.

        Yields
        ------
        bytes
            Each line read from the serial channel.
        """
        while line := self.channel.readline():
            yield line
        print("Reception ended. No data received after timeout of", self.channel.timeout, "seconds.")