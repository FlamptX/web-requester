from discord import Embed
from .colors import Color

class ResponseEmbed(Embed):
    def __init__(self, response):
        super().__init__()
        self.title = 'Request response'
        self.description = f'```{response}```'
        self.color = Color.green

class IncorrectURL(Embed):
    def __init__(self, url):
        super().__init__()
        self.title = 'Incorrect URL'
        self.description = f'`{url}` does not exist, double check it and try again.'
        self.color = Color.red

class UnexpectedKeyEmbed(Embed):
    def __init__(self, key, method):
        super().__init__()
        self.title = 'Unexpected Key'
        self.description = f'`{key}` key was unexpected in {method} method.'
        self.color = Color.red

class InvalidURLEmbed(Embed):
    def __init__(self, url):
        super().__init__()
        self.title = 'Invalid URL'
        self.description = f'`{url}` is not a valid URL. Make sure that it starts with http/s and has valid characters.'
        self.color = Color.red

class InvalidHeadersEmbed(Embed):
    def __init__(self, error):
        super().__init__()
        self.title = 'Invalid Headers'
        self.description = f'Exception occurred when reading the headers:\n```{error}```'
        self.color = Color.red

class InvalidDataEmbed(Embed):
    def __init__(self, error):
        super().__init__()
        self.title = 'Invalid Data'
        self.description = f'Exception occurred when reading the data:\n```{error}```'
        self.color = Color.red
