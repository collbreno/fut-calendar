from unidecode import unidecode
import re

class IDUtils:
    @staticmethod
    def generateID(*args):
        pattern = r'[^a-v0-9]'
        id = ''
        for arg in args:
            r = str(arg)
            r = r.lower()
            r = unidecode(r)
            r = re.sub(pattern, '', r)
            id += r
        return id

