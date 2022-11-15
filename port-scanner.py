import pyfiglet
import socket
import threading
from queue import Queue

scannerBanner = pyfiglet.figlet_format("PORT SCANNER")
print(scannerBanner)
# Use your router ip address or localhost(127.0.0.1) or you can use other networks ip when you have it's permission.
HOST = ""
QUEUE = Queue()
ACTIVE_PORTS = []
THREAD_LIST = []

def scanPort(PORT):
    ADDR = (HOST, PORT)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(ADDR)
        return True
    except:
        return False

def addToQueue(PORTRANGE):
    for PORT in range(PORTRANGE[0], PORTRANGE[1]):
        QUEUE.put(PORT)

def operator():
    while not QUEUE.empty():
        PORT = QUEUE.get()
        if scanPort(PORT):
            print(f"Port {PORT} is open!")
            ACTIVE_PORTS.append(PORT)

FROM = int(input("Enter the start port of range to scan: "))
TO = int(input("Enter the end port of range to scan: "))
addToQueue(PORTRANGE=(FROM, TO+1))

# Increasing the number of threads faster scaning ports.
# It's not preferred to use a large number of threads. In my case, 500/1000 is enough.
for _ in range(1000):
    thread = threading.Thread(target=operator)
    THREAD_LIST.append(thread)

# Start all the threads
for THREAD in THREAD_LIST:
    THREAD.start()

# Wait until all threads are completely executed.
for THREAD in THREAD_LIST:
    THREAD.join()

print("Open ports are: ", ACTIVE_PORTS)