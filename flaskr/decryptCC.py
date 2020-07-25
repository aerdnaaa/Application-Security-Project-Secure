import pyffx
e = pyffx.Integer(b'12376987ca98sbdacsbjkdwd898216jasdnsd98213912', length=16)
creditcardno = '2654859379613343'
print(e.decrypt(creditcardno))