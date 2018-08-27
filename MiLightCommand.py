import logging
import socket
import time

from AppSettingsProvider import AppSettingsProvider

LOGGER = logging.getLogger(__name__)

class MiLightCommand(object):
    # all bridge commands are 3 bytes:
    # 1 byte is the operator
    # 2 byte is 0x00 (0) or a value for specific operators when setting color or brightness
    # 3 byte is always a suffix of 0x55 (85)

    # static variable to keep track of when the previous command was sent
    LastCommandTime = time.time()

    # lights require time between commands, 100ms is recommended by the documentation
    PAUSE = 0.1
    # bridge details from appSettings
    SETTINGS = AppSettingsProvider().get_miLight_settings()

    def __init__(self, operator, value=None):
        self._operator = operator
        self._value = bytes([0]) if value is None else value
        self._terminator = bytes([85])

    def send(self):
        """ Dispatch command via udp to miLight bridge """

        current_pause = time.time() - MiLightCommand.LastCommandTime
        if current_pause < self.PAUSE:
            time.sleep(self.PAUSE - current_pause)

        LOGGER.info('Dispatching udp command to miLight bridge')
        MiLightCommand.LastCommandTime = time.time()

        command = self._operator + self._value + self._terminator
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udpSocket: # Internet, UDP
            udpSocket.sendto(command, (self.SETTINGS.BridgeIp, self.SETTINGS.BridgePort))