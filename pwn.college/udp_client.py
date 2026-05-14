import socket
import time

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("0.0.0.0", 31337))


for p in range(1024,65535):
    for i in range(1):
        s.sendto(b"FLAG:10.0.0.1:4242", ("10.0.0.2", p))
        #time.sleep(0.3)

exit()

x = s.recvfrom(1024)
print(x)

"""
s.bind(("0.0.0.0", 31338))
s.sendto(b"ACTION?", ("10.0.0.2", 31337))
message, (peer_host, peer_port) = s.recvfrom(1024)

print(message)

if peer_port == 31337 and message.strip() == b"FLAG":
    print(f"YOUR FLAG: {flag}")
"""
