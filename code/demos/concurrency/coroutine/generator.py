import random
import resource

THREADS = 1_000_000

def T_worker(name):
    i = 0
    while (i := i + 1):
        yield f"[{name}] i = {i}"

threads = [T_worker(i) for i in range(THREADS)]

count = 0
while count < 10_000_000:
    current = random.choice(threads)
    res = current.send(None)
    print(res)

    count += 1
