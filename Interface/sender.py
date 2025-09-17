from interpreter import Transfer

def send_packet(channel:Transfer,description: bytes, data:bytes):
    if len(description) != 8:
        raise ValueError("Description must be exactly 8 bits long.")
    if len(data) != 16:
        raise ValueError("Data must be exactly 16 bits long.")
    
    packet = description + data
    channel.send(packet)

#Example usage
mainline = Transfer("COM3", timeout=3)

send_packet(mainline, b'10101010', b'1111100000000000')