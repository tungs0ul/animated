import time
import datetime

a = time.time()
for i in range(10000):
    i**2
b = time.time()

print(b-a)