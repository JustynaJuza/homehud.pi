import logging

from ArgumentParser import debuggingOnPC

from ApiHandler import ApiHandler
from MiLightSwitcher import MiLightSwitcher
from EnergenieLightSwitcher import EnergenieLightSwitcher

LOGGER = logging.getLogger(__name__)

class Light(object):

   def __init__(self, id, state, color = None, brightness = None):
        self.Id = id
        self.State = state
        self.Color = color
        self.Brightness = brightness

class MessageProcessingService(object):

    def __init__(self, requestServer):
        self._api = ApiHandler()
        self._hostUrl = requestServer.ServerLocal if debuggingOnPC else requestServer.ServerExternal
        self._lightsPath = requestServer.ConfirmLights
        self._antiforgeryTokenPath = requestServer.AntiforgeryToken

    def format_url(self, host, path):
        return '{0}/{1}'.format(host, path)

    def process_message(self, message):
        try:

            messageParts = message.decode().split(',')
            miLightSwitcher = MiLightSwitcher()
            if miLightSwitcher.has_message_prefix(messageParts):
                LOGGER.info('Processing MiLight switch command')

                lightGroup = messageParts[1].strip()
                command = messageParts[2].strip()
                value = int(messageParts[3].strip()) if len(messageParts) >= 4 else None

                miLightSwitcher.switch_lights(lightGroup, command, value)

            else:
                LOGGER.info('Processing Energenie switch command')

                lightState = int(messageParts[0].strip())
                lightIdsStr = messageParts[1].strip().split(' ')
                # if no light ids provided means all lights should be switched to lightState
                # mapping to list since otherwise would be lazily evaluated and would cause mayhem!
                lightIds = list(map(int, lightIdsStr)) if lightIdsStr != [''] else None

                lightSwitcher = EnergenieLightSwitcher()
                lightSwitcher.switch_lights(lightState, lightIds)

                # update state on homeHud website
                # TODO: Move this somewhere
                lightsState = []
                for piLight in lightSwitcher.LIGHTS:
                    light = Light(piLight.Id, piLight.State)
                    lightsState.append(light)

                self._api.postJsonWithAntiforgery(
                    url=self.format_url(self._hostUrl, self._lightsPath),
                    antiforgeryPath=self.format_url(self._hostUrl, self._antiforgeryTokenPath),
                    data=lightsState,
                    params=None)

        except ValueError:
            LOGGER.error('Parsing message {0} failed'.format(message))