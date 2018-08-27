class RabbitMqCredentials(object):

   def __init__(self, username, password, server, port, virtualHost):
        self.Username = username
        self.Password = password
        self.Server = server
        self.Port = port
        self.VirtualHost = virtualHost

class RabbitMqQueue(object):

   def __init__(self, name, durable, autoDelete, noAck, exclusive):
        self.Name = name
        self.Durable = durable
        self.AutoDelete = autoDelete
        self.NoAck = noAck
        self.Exclusive = exclusive

class HomeHud(object):

    def __init__(self, serverLocal, serverExternal, antiforgeryToken, confirmLights):
        self.ServerLocal = serverLocal
        self.ServerExternal = serverExternal
        self.AntiforgeryToken = antiforgeryToken
        self.ConfirmLights = confirmLights

class MiLightSettings(object):

    def __init__(self, bridgeIp, bridgePort):
        self.BridgeIp = bridgeIp
        self.BridgePort = int(bridgePort)

class MiLightFormatting(object):

   def __init__(self, miLightPrefix, commands):
        self.Prefix = miLightPrefix
        self.Commands = commands