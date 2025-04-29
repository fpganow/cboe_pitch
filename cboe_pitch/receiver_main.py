"""
Receiver

Enumerates all Serial Port / COM connections available on the current
computer.

Linux: List devices in /dev/ that start with tty, e.g., /dev/ttyUSB0 or /dev/ttyACM0.
Requirements:
- pyserial
"""

import argparse
from typing import Any

import serial
import serial.tools.list_ports
import time

def enumerate_all():
    """
COM3: Intel(R) Active Management Technology - SOL (COM3) [PCI\VEN_8086&DEV_02E3&SUBSYS_22BE17AA&REV_00\3&11583659&0&B3]
COM4: Standard Serial over Bluetooth link (COM4) [BTHENUM\{00001101-0000-1000-8000-00805F9B34FB}_VID&0001005D_PID&0000\7&18125ADC&0&000A4523B0AC_C00000000]
COM5: Standard Serial over Bluetooth link (COM5) [BTHENUM\{00001101-0000-1000-8000-00805F9B34FB}_LOCALMFG&0000\7&18125ADC&0&000000000000_00000002]
COM9: USB Serial Port (COM9) [USB VID:PID=0403:6010 SER=003017B7EAFDB]
    """
    ports = serial.tools.list_ports.comports()
    for port in sorted(ports):
        print(f'port.vid: {port.vid}')
        print(f'port.device: {port.device}')
        print(f'port.hwid: {port.hwid}')
        print(f'port.hwid: {port.manufacturer}')
        print(f'port.hwid: {port.name}')
        print(f'port.hwid: {port.description}')
        print(f'port.hwid: {port.serial_number}')
    for port, desc, hwid in sorted(ports):
        print(f"{port}: {desc} [{hwid}]")
        if port == "COM9":
            
            #breakpoint()
            print("TARGET")
        #print(f" - {port}")

def listen_to(com_port: str, baud_rate: int = 115_200) -> None:
    """
    """
      # Replace 'COMx' or '/dev/tty...' with the actual port name
    port = serial.Serial(
        port=com_port, # Example Windows port
        baudrate=baud_rate,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
    )
    print("Connected to: " + port.portstr)
    
    while True:
        try:
            if port.in_waiting > 0:
                data = port.readline().decode('utf-8').rstrip()
                print(data)
        except serial.SerialException:
            print("Serial connection lost.")
            break
        except UnicodeDecodeError:
             print("Could not decode data")
        time.sleep(0.1)
    
    port.close()

def parse_args() -> Any:
    parser = argparse.ArgumentParser(
        prog="Receiver",
        description="Normalized Message Receiver",
        epilog="Bottom of help text",
    )
    parser.add_argument(
        "-v", "--verbose", default=False, action="store_true", help="Verbose"
    )
    parser.add_argument(
        "-d", "--debug", default=False, action="store_true", help="Debug"
    )

    return parser.parse_args()

def main():
    """
    Baud Rate: 115200
    Data Bits: 8
    Stop Bits: 1
    Parity: None
    Flow Control: None
    """
    args = parse_args()

    print('Receiver')
    enumerate_all()

    listen_to("COM9")

if __file__ == "__main__" or __name__ == "__main__":
    main()
