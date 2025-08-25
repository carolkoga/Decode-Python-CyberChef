import base64

KEY=0x3
PLAIN = b"""BEGIN_PAYLOAD
URL=http://malicious.example/update.bin
C2=198.51.100.42:8080
Mutex=Global\Updater_123
UA=Mozilla/5.0 (Windows NT 10.0; Win64; x64)
END_PAYLOAD
"""

with open("payload/payload_plain.txt","wb")as f:
    f.write(PLAIN)

xored=bytes([b^KEY for b in PLAIN])
base64 = base64.b64encode(xored)

with open("payload/payload_obfuscated.txt"):
print("Chave XOR (hex):0x{:02}".format(KEY))