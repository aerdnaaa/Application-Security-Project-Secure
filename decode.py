import base64
import zlib

def decodeSession(session):
    print(zlib.decompress(base64.urlsafe_b64decode('{}==='.format(session))))

decodeSession('eJwlzjtuAzEMRdG9qE5BURQlejMD8QcbARJgxq6C7N0K0rziFg_npxx5xnUvt-f5io9yPLzcCngfWdGZdGJtfdqACNyTPZQAe2sqLQkIOUFIGsIYhkAqHZlMVKdVnbwYQcCShNzSZ3gzFU0VHqS43GvWRR1Wt2BbqaajbMjrivNfUxvBLnadeTy_P-Prr22KKdpIskViyepr7E_sshCUHbwqcvl9A2unQLg')


