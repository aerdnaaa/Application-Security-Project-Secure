import base64
import zlib

def decodeSession(session):
    print(zlib.decompress(base64.urlsafe_b64decode('{}==='.format(session))))

decodeSession('')
