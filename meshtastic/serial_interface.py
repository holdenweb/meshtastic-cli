""" Serial interface class
"""
import logging
import platform
import time

import serial  # type: ignore[import-untyped]

import meshtastic.util
from meshtastic.stream_interface import StreamInterface

if platform.system() != "Windows":
    import termios


class SerialInterface(StreamInterface):
    """Interface class for meshtastic devices over a serial link"""

    def __init__(self, devPath=None, debugOut=None, noProto=False, connectNow=True):
        """Constructor, opens a connection to a specified serial port, or if unspecified try to
        find one Meshtastic device by probing

        Keyword Arguments:
            devPath {string} -- A filepath to a device, i.e. /dev/ttyUSB0 (default: {None})
            debugOut {stream} -- If a stream is provided, any debug serial output from the device will be emitted to that stream. (default: {None})
        """
        self.noProto = noProto
        self.devPath = devPath
        if self.devPath is None:
            ports = meshtastic.util.findPorts(True)
            logging.debug(f"ports:{ports}")
            if len(ports) == 0:
                # This was formerly a return, which bypassed the call to
                # super().__init__, leading to downstream issues. Hopefully
                # the exception will make handling easier. It certainly isn't
                # the serial interface's role to say what happens next if it
                # can't find an appropriate serial device.
                raise OSError("No serial Meshtastic device detected - please specify using '--port'")
            elif len(ports) > 1:
                raise OSError(
                    f"""Multiple serial ports were detected - use the '--port' option
to choose one of {', '.join(ports)}"""
                )
            else:
                self.devPath = ports[0]
        logging.debug(f"Connecting to {self.devPath}")
        self.stream = serial.Serial(
            self.devPath, 115200, exclusive=True, timeout=0.5, write_timeout=0
        )
        self.stream.flush()
        time.sleep(0.1)
        #
        # At present, due to the structure of the code, it's hard to tell
        # exactly when it's OK to call super()_.__init__.
        super().__init__(debugOut=debugOut, noProto=noProto, connectNow=connectNow)
        # first we need to set the HUPCL so the device will not reboot based on RTS and/or DTR
        # see https://github.com/pyserial/pyserial/issues/124
        if platform.system() != "Windows":
            with open(self.devPath, encoding="utf8") as f:
                attrs = termios.tcgetattr(f)
                attrs[2] = attrs[2] & ~termios.HUPCL
                termios.tcsetattr(f, termios.TCSAFLUSH, attrs)
                f.close()
            time.sleep(0.1)

    def close(self):
        """Close a connection to the device"""
        self.stream.flush()
        time.sleep(0.1)
        self.stream.flush()
        time.sleep(0.1)
        logging.debug("Closing Serial stream")
        StreamInterface.close(self)
