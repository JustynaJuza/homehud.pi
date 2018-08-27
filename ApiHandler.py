import requests
import logging
import json

LOGGER = logging.getLogger(__name__)

class AntiforgeryToken:

    def __init__(self):
        self.HeaderName = ''
        self.Token = ''
        self.Cookies = None

    def fromJson(self, dict):
        self.HeaderName = dict['headerName']
        self.Token = dict['token']

    def formatHeaderToken(self):
        return { self.HeaderName : self.Token }

class ApiHandler(object):

    def __init__(self):
        return

    def serialize_as_dict(self, obj):
        return obj.__dict__

    def getAntiforgeryToken(self, url):
        LOGGER.info('Requesting token from {0}'.format(url))
        response = requests.get(url)

        if response.status_code == requests.codes.ok:
            LOGGER.info('Token request sent to {0} responded OK'.format(url)) 
            antiforgeryToken = AntiforgeryToken()
            json.loads(response.content.decode('utf-8'), object_hook=antiforgeryToken.fromJson)

            antiforgeryToken.Cookies = response.cookies
            return antiforgeryToken
        else:
            LOGGER.error('POST request sent to {0} responded with error code {1}: {2}'.format(url, response.status_code, response.text))
            return None

    def getJson(self, url, params=None):
        response = requests.get(url, params)

        if response.status_code == requests.codes.ok:
            LOGGER.info('GET request sent to {0} responded OK'.format(url))
            return json.loads(response.content)
        else:
            LOGGER.error('GET request sent to {0} responded with error code {1}: {2}'.format(url, response.status_code, response.text))


    def postJson(self, url, params, data, headers=None, cookies=None):

        jsonData=json.dumps(data, default=self.serialize_as_dict)
        # random hack to prevent requests.post escaping double quotes with \\
        # basically replaces double quotes with single quotes, supposedly parsing to Python objects, pff
        # God knows why this works, maybe I'll learn someday
        otherJson = json.loads(jsonData)

        LOGGER.info('Sending json data to {0} with parameters {1}: \n{2}'
            .format(url, params, otherJson))
        response = requests.post(url, data=params, json=otherJson, headers=headers, cookies=cookies)

        if response.status_code == requests.codes.ok:
            LOGGER.info('POST request sent to {0} responded OK'.format(url))
            return response.text
        else:
            LOGGER.error('POST request sent to {0} responded with error code {1}: {2}'.format(url, response.status_code, response.text))

    def postJsonWithAntiforgery(self, url, params, data, antiforgeryPath):
        antiforgeryToken = self.getAntiforgeryToken(antiforgeryPath)

        return self.postJson(url, params, data,
            headers=antiforgeryToken.formatHeaderToken(),
            cookies=antiforgeryToken.Cookies)