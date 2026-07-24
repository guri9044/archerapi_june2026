import base64
with open('session.jpg',"rb") as file:
    bytes = file.read()
bytearray = bytearray(bytes)
print(bytes)

print(base64.encodebytes(bytearray))