import time
import sys

if (len(sys.argv)) != 3:
    print(f"Usage: ./djinn.py IP PORT")
    sys.exit(0)

IP=sys.argv[1]
PORT=sys.argv[2]
print(f"Connecting to the host: {IP}:{PORT}")

class col:
    RED = '\033[31m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    RESET = '\033[0m'

def calcnumbers(num1, num2, calc):
    if calc == "/":
        return num1 / num2
    elif calc == "*":
        return num1 * num2
    elif calc == "+":
        return num1 + num2
    elif calc == "-":
        return num1 - num2

def parseResponse(question, s, count):
    question =  str(question)
    mathQ = question.split("\n")
    if len(mathQ) == 2:
        mathQ = mathQ[0]
    else:
        mathQ = mathQ[3]
       
    num1 = mathQ.split("(")[1].split(",")[0].strip()
    num2 = mathQ.split(",")[2].split(")")[0].strip()
    calc = mathQ.split("'")[1].split("'")[0].strip()
    #change to int
    num1 = int(num1)
    num2 = int(num2)
    #Work out numbers
    answer = calcnumbers(num1, num2, calc)
    
    print(f"Trying: {count}: {num1} {calc} {num2} = {answer}, Sent: {answer}\n")
    answer = str(answer) + "\n"
    s.send(answer.encode())
    r = s.recv(4096)
    r += s.recv(2048)
    count +=1
    return r

time.sleep(1)
try:            
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((IP, int(PORT)))
        welcome = s.recv(2048)
        print(welcome.decode())
        time.sleep(2)
        r = s.recv(2048)
        question = r.decode()
        
        for i in range(0,1001):
            a =  parseResponse(question, s, i)
            if "Here" in str(a):
                print(col.GREEN+  f"Result:\n{a.decode()}\n" + col.RESET)
            question = a.decode()
except Exception as e:
    print(col.RED + f"Connection died, try again.\n"+ col.RESET +  f"\nError: {e}")  
