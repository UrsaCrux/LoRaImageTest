from interpreter import Transfer

def send_packet(channel:Transfer, description: int, data:int, ashex:bool=True):
    #Extracts the bytes ignoring leading zeroes
    desc = int.to_bytes(description, 1, 'big')
    dat = int.to_bytes(data, 2, 'big')

    #Concats
    packet = desc + dat
    #Data output
    if ashex:
        print(f"Sending packet: {packet.hex()}")
    else:
        bit_str = ''.join(f'{byte:08b}' for byte in packet)
        print(f"Sending packet: {bit_str}")
    
    #Sending the packet
    channel.send(packet)

#Example usage
mainline = Transfer("COM3", timeout=3)

#Declare a byte with 0b
send_packet(mainline, 0b10101001, 0b1111100000000000, ashex=False)
#Declare a hex with 0x
send_packet(mainline, 0xa9, 0xf800)