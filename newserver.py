import socket
import sys
from time import sleep

# create an INET, STREAMing socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(5)
# now connect to the web server on port 80 - the normal http port
s.connect(("i-regul.fr", 443))

# 501 => request DATA refresh
# 502 => DATA + Nom propre
#

s.send("cdraminfo106949TWHQWC{502#}".encode())

while True:
    try:
        msg = s.recv(8192)
    except socket.timeout as e:
        err = e.args[0]
        # this next if/else is a bit redundant, but illustrates how the
        # timeout exception is setup
        if err == "timed out":
            sleep(1)
            print("recv timed out, retry later")
            continue
        else:
            print(e)
            sys.exit(1)
    except socket.error as e:
        # Something else happened, handle error, exit, etc.
        print(e)
        sys.exit(1)
    else:
        if len(msg) == 0:
            print("orderly shutdown on server end")
            sys.exit(0)
        else:
            print(msg.decode("utf-8"))
