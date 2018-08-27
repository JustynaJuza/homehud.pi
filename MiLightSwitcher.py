from ArgumentParser import debuggingOnPC
from AppSettingsProvider import AppSettingsProvider
from MiLightGroups import MiLightColorGroup

class MiLightSwitcher(object):

    FORMATTING = AppSettingsProvider().get_miLight_formatting()

    def __init__(self):
        return

    def has_message_prefix(self, messageParts):
        return messageParts[0] == self.FORMATTING.Prefix

    def switch_lights(self, lightGroup, command, value):
        group = MiLightColorGroup(lightGroup)
        group.resolve_command(command, value)