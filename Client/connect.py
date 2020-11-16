import subprocess
# import socket
# import fcntl
# import struct

out = subprocess.check_output("netsh wlan show interfaces").decode('utf-8')
print(out)
