"""Simple program to demo how to use meshtastic library.
   To run: python examples/hello_world_serial.py
"""

import sys

import meshtastic
import meshtastic.serial_interface

# simple arg check: we do expect a message, or what's the point?
if len(sys.argv) < 2:
    print(f"usage: {sys.argv[0]} message")
    sys.exit(3)

# By default will try to find a meshtastic device,
# otherwise provide a device path like /dev/ttyUSB0
# as an argument.
try:
    iface = meshtastic.serial_interface.SerialInterface()
except OSError as e:
    print(e, file=sys.stderr)
    sys.exit(2)
iface.sendText(sys.argv[1])
iface.close()
