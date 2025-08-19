import threading
import time

def worker(name: str):
    print(f"Thread {name} starting")
    time.sleep(0.1)
    print(f"Thread {name} finished")

t1 = threading.Thread(target=worker, args=("Atyantik",))
t2 = threading.Thread(target=worker, args=("Google",))

t1.start()
t2.start()

t1.join()
t2.join()

print("Both threads completed")