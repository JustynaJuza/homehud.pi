import logging

from MiLightCommand import MiLightCommand

LOGGER = logging.getLogger(__name__)

class MiLightGroup(object):

    GROUP_ON = {
        'ALL': bytes([66]),
        '1': bytes([69]),
        '2': bytes([71]),
        '3': bytes([73]),
        '4': bytes([75])
    }

    GROUP_OFF = {
        'ALL': bytes([65]),
        '1': bytes([70]),
        '2': bytes([72]),
        '3': bytes([74]),
        '4': bytes([76])
    }

    def __init__(self, groupNumber):
        self._group = str(groupNumber) if str(groupNumber) in ['1', '2', '3', '4'] else 'ALL'

    def on(self):
        """ Switch group on """
        LOGGER.info('Swiching lights ON in group {0}'.format(self._group))
        MiLightCommand(self.GROUP_ON[self._group]).send()

    def off(self):
        """ Switch group off """

        LOGGER.info('Swiching lights OFF in group {0}'.format(self._group))
        MiLightCommand(self.GROUP_OFF[self._group]).send()


class MiLightColorGroup(MiLightGroup):
    """ A group of RGBW color bulbs/strips """

    GROUP_WHITE = {
        'ALL': bytes([194]),
        '1': bytes([197]),
        '2': bytes([199]),
        '3': bytes([201]),
        '4': bytes([203])
    }

    BRIGHTNESS = bytes([78])

    COLOR = bytes([64])

    COLOR_CODES = {
        "VIOLET": b"\x00",
        "ROYALBLUE": b"\x10",
        "LIGHTSKYBLUE": b"\x20",
        "AQUA": b"\x30",
        "AQUAMARINE": b"\x40",
        "SEAGREEN": b"\x50",
        "GREEN": b"\x60",
        "LIMEGREEN": b"\x70",
        "YELLOW": b"\x80",
        "GOLDENROD": b"\x90",
        "ORANGE": b"\xA0",
        "RED": b"\xB0",
        "PINK": b"\xC0",
        "FUCHSIA": b"\xD0",
        "ORCHID": b"\xE0",
        "LAVENDER": b"\xF0"
    }

    DISCO_MODE = bytes([77])
    DISCO_SPEED_SLOWER = bytes([67])
    DISCO_SPEED_FASTER = bytes([68])

    DISCO_CODE = b"\x42\x00\x40\x40\x42\x00\x4e\x02"
    DISCO_CODES = {
        "RAINBOW": b"\x4d\x00" * 1,
        "WHITE BLINK": b"\x4d\x00" * 2,
        "COLOR FADE": b"\x4d\x00" * 3,
        "COLOR CHANGE": b"\x4d\x00" * 4,
        "COLOR BLINK": b"\x4d\x00" * 5,
        "RED BLINK": b"\x4d\x00" * 6,
        "GREEN BLINK": b"\x4d\x00" * 7,
        "BLUE BLINK": b"\x4d\x00" * 8,
        "DISCO": b"\x4d\x00" * 9
    }


    def __init__(self, groupNumber):
        super().__init__(groupNumber)

    def resolve_command(self, commandName, value):
        {
            'ON': lambda _: self.on(),
            'OFF': lambda _: self.off(),
            'WHITE': lambda _: self.set_white(),
            'BRIGHTNESS': lambda value: self.set_brightness(value),
            'COLOR': lambda value: self.set_color(value),
            'DISCO': lambda mode: self.set_disco(mode)
        }[commandName](value)

    def set_white(self):
        """ Switch to white """

        LOGGER.info('Swiching lights to white in group {0}'.format(self._group))
        MiLightCommand(self.GROUP_WHITE[self._group]).send()

    def set_brightness(self, value=25):
        # byte2: 0x02 to 0x1B (2-27)
        """ Set brightness level (0-25) """

        value = max(0, min(25, value))
        value += 2

        self.on()
        LOGGER.info('Swiching light brightness to {1} in group {0}'.format(self._group, value))
        MiLightCommand(self.BRIGHTNESS, bytes[(value)]).send()

    def set_color(self, hueValue):
        # byte2: 0x00 to 0xFF (255 colors)
        """ Set color hue (0-255) """

        hueValue = max(0, min(255, hueValue))

        self.on()
        LOGGER.info('Swiching light color to {1} in group {0}'.format(self._group, hueValue))
        MiLightCommand(self.COLOR, bytes([hueValue])).send()


    def set_disco(self, mode=''):
        """ Enable disco mode, if no valid mode is provided the default disco mode is started """
        self.on()
        if mode.upper() in self.DISCO_CODES:
            command = self.DISCO_CODE + self.DISCO_CODES[mode.upper()]
            self.send_command(command, byte2=b"", byte3=b"")
        else:
            self.send_command(self.DISCO_MODE)

    def increase_disco_speed(self, steps=1):
        """ Increase disco_speed (1 <= value <= 30) """
        steps = max(1, min(30, steps))  # value should be between 1 and 30
        self.on()
        for i in range(0, steps):
            self.send_command(self.DISCO_SPEED_FASTER)

    def decrease_disco_speed(self, steps=1):
        """ Decrease disco_speed (1 <= value <= 30) """
        steps = max(1, min(30, steps))  # value should be between 1 and 30
        self.on()
        for i in range(0, steps):
            self.send_command(self.DISCO_SPEED_SLOWER)

    def disco_codes(self):
        """ return the disco-codes """
        return [c for c in self.DISCO_CODES.keys()]


#class WhiteGroup(Group):
#    """ A group of white bulbs/strips """

#    # Standard ON/OFF
#    WHITE_ALL_ON = (53).to_bytes(1, byteorder='big')
#    WHITE_ALL_OFF = (57).to_bytes(1, byteorder='big')
#    GROUP_1_ON = (56).to_bytes(1, byteorder='big')
#    GROUP_1_OFF = (59).to_bytes(1, byteorder='big')
#    GROUP_2_ON = (61).to_bytes(1, byteorder='big')
#    GROUP_2_OFF = (51).to_bytes(1, byteorder='big')
#    GROUP_3_ON = (55).to_bytes(1, byteorder='big')
#    GROUP_3_OFF = (58).to_bytes(1, byteorder='big')
#    GROUP_4_ON = (50).to_bytes(1, byteorder='big')
#    GROUP_4_OFF = (54).to_bytes(1, byteorder='big')

#    GROUP_ON = {
#        'ALL': WHITE_ALL_ON,
#        '1': GROUP_1_ON,
#        '2': GROUP_2_ON,
#        '3': GROUP_3_ON,
#        '4': GROUP_4_ON
#    }
#    GROUP_OFF = {
#        'ALL': WHITE_ALL_OFF,
#        '1': GROUP_1_OFF,
#        '2': GROUP_2_OFF,
#        '3': GROUP_3_OFF,
#        '4': GROUP_4_OFF
#    }

#    # Standard BRIGHTNESS/WHITE-COLOR
#    BRIGHTNESS_UP = (60).to_bytes(1, byteorder='big')
#    BRIGHTNESS_DOWN = (52).to_bytes(1, byteorder='big')
#    WARM_WHITE_INCREASE = (62).to_bytes(1, byteorder='big')
#    COOL_WHITE_INCREASE = (63).to_bytes(1, byteorder='big')

#    # Specials FULL_BRIGHTNESS/NIGHT_MODE
#    FULL_BRIGHTNESS_ALL = (181).to_bytes(1, byteorder='big')  # send 100ms after GROUP_ON
#    FULL_BRIGHTNESS_GROUP_1 = (184).to_bytes(1, byteorder='big')  # send 100ms after GROUP_ON
#    FULL_BRIGHTNESS_GROUP_2 = (189).to_bytes(1, byteorder='big')  # send 100ms after GROUP_ON
#    FULL_BRIGHTNESS_GROUP_3 = (183).to_bytes(1, byteorder='big')  # send 100ms after GROUP_ON
#    FULL_BRIGHTNESS_GROUP_4 = (178).to_bytes(1, byteorder='big')  # send 100ms after GROUP_ON
#    # send 100ms after GROUP_OFF
#    NIGHT_MODE_ALL = (185).to_bytes(1, byteorder='big')
#    NIGHT_MODE_GROUP_1 = (187).to_bytes(1, byteorder='big')  # send 100ms after GROUP_OFF
#    NIGHT_MODE_GROUP_2 = (179).to_bytes(1, byteorder='big')  # send 100ms after GROUP_OFF
#    NIGHT_MODE_GROUP_3 = (186).to_bytes(1, byteorder='big')  # send 100ms after GROUP_OFF
#    NIGHT_MODE_GROUP_4 = (182).to_bytes(1, byteorder='big')  # send 100ms after GROUP_OFF

#    FULL_BRIGHTNESS = {  # send 100ms after GROUP_ON
#        'ALL': FULL_BRIGHTNESS_ALL,
#        '1': FULL_BRIGHTNESS_GROUP_1,
#        '2': FULL_BRIGHTNESS_GROUP_2,
#        '3': FULL_BRIGHTNESS_GROUP_3,
#        '4': FULL_BRIGHTNESS_GROUP_4
#    }
#    NIGHT_MODE = {  # send 100ms after GROUP_OFF
#        'ALL': NIGHT_MODE_ALL,
#        '1': NIGHT_MODE_GROUP_1,
#        '2': NIGHT_MODE_GROUP_2,
#        '3': NIGHT_MODE_GROUP_3,
#        '4': NIGHT_MODE_GROUP_4
#    }

#    def __init__(self, ip_address, port=8899, pause=0.1, group_number=None):
#        """ init """
#        super().___init___(ip_address, port, pause, group_number)

#    def increase_brightness(self, steps=1):
#        """ Increase brightness (1 <= value <= 30) """
#        steps = max(1, min(30, steps))  # value should be between 1 and 30
#        self.on()
#        for i in range(0, steps):
#            self.send_command(self.BRIGHTNESS_UP)

#    def decrease_brightness(self, steps=1):
#        """ Decrease brightness (1 <= value <= 30) """
#        steps = max(1, min(30, steps))  # value should be between 1 and 30
#        self.on()
#        for i in range(0, steps):
#            self.send_command(self.BRIGHTNESS_DOWN)

#    def increase_warmth(self, steps=1):
#        """ Increase warmth (1 <= value <= 30) """
#        steps = max(1, min(30, steps))  # value should be between 1 and 30
#        self.on()
#        for i in range(0, steps):
#            self.send_command(self.WARM_WHITE_INCREASE)

#    def decrease_warmth(self, steps=1):
#        """ Decrease warmth (1 <= value <= 30) """
#        steps = max(1, min(30, steps))  # value should be between 1 and 30
#        self.on()
#        for i in range(0, steps):
#            self.send_command(self.COOL_WHITE_INCREASE)

#    def brightmode(self):
#        """ Enable full brightness """
#        self.on()
#        self.send_command(self.FULL_BRIGHTNESS[self.group])

#    def nightmode(self):
#        """ Enable nightmode """
#        self.off()
#        self.send_command(self.NIGHT_MODE[self.group])
