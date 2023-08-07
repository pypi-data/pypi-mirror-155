"""
This module is used to discover the serial address of any ML600 connected to the PC.
"""
import serial.tools.list_ports
from loguru import logger

from flowchem.components.devices.Harvard_Apparatus.HA_elite11 import (
    HarvardApparatusPumpIO,
)
from flowchem.exceptions import InvalidConfiguration


# noinspection PyProtectedMember
def elite11_finder():
    """Try to initialize an Elite11 on every available COM port."""
    port_available = [comport.device for comport in serial.tools.list_ports.comports()]

    # Ports connected to an elite11-looking device
    valid_ports = set()

    for serial_port in port_available:
        try:
            print(f"Looking for pump on {serial_port}...")
            link = HarvardApparatusPumpIO(port=serial_port)
            link._serial.write("\r\n".encode("ascii"))
            if link._serial.readline() == b"\n":
                valid_ports.add(serial_port)
                logger.info(f"Pump found on <{serial_port}>")
                pump = link._serial.readline().decode("ascii")
                logger.info(f"Pump address is {pump[0:2]}!")
                print(f"Found a pump with address {pump[0:2]} on {serial_port}!")
            else:
                logger.debug(f"No pump found on {serial_port}")
        except InvalidConfiguration:
            pass

    return valid_ports


if __name__ == "__main__":
    elite11_pumps = elite11_finder()
    if len(elite11_pumps) > 0:
        print(f"The following serial port are connected to Elite11: {elite11_pumps}")
    else:
        print("No Elite11 pump found")
