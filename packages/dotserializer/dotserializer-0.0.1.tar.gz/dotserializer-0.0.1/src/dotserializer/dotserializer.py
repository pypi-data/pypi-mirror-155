import struct

import serial
import serial.tools.list_ports


class Serializer:
    END = b"\x0A"
    ESC = b"\x0B"
    ESC_END = b"\x1A"
    ESC_ESC = b"\x1B"

    def __init__(self, port=None, baudrate=115200, timeout=None):
        self._port = port
        self.baudrate = baudrate
        self.timeout = timeout

        if not self._port:
            # if no port is supplied, we enumerate the available ports
            # and try the first one
            ports = Serializer.getAvailablePorts()
            if ports:
                self._port = ports[0]
                print(
                    "No \"port\" argument supplied, using {0}.".format(self._port))

        self._ser = serial.Serial(
            port=self._port, baudrate=baudrate, timeout=timeout)

    @staticmethod
    def getAvailablePorts():
        ports = [p.name for p in serial.tools.list_ports.comports()]
        return ports

    """
    Receive a packet from serial.

    @return:
    """
    def receive(self):
        c = b""
        buffer = b""
        while c != Serializer.END:
            if c == Serializer.ESC:
                c = self._ser.read(1)
                if c == Serializer.ESC_END:
                    buffer += Serializer.END
                elif c == Serializer.ESC_ESC:
                    buffer += Serializer.ESC
                else:
                    buffer += c
            else:
                buffer += c
            c = self._ser.read(1)
            if c == b"":
                return buffer
        return buffer

    """
    Transmit a packet to serial.

    @type buffer: bytes
    @param buffer: the data buffer that will be sent.
    """
    def transmit(self, buffer):
        if type(buffer) == str:
            raise AttributeError(
                "cannot transmit \"str\" object. Perhaps try \"str.encode()\" it?")

        index = 0
        while index < len(buffer):
            c = struct.pack("B", buffer[index])
            if c == Serializer.END:
                self._ser.write(Serializer.ESC)
                self._ser.write(Serializer.ESC_END)
            elif c == Serializer.ESC:
                self._ser.write(Serializer.ESC)
                self._ser.write(Serializer.ESC_ESC)
            else:
                self._ser.write(c)
            index += 1
        self._ser.write(Serializer.END)
