import random
import time


BITS_LENGTH = [40, 56, 80, 128, 168, 224, 256, 512, 1024, 2048, 4096]


def lcg(m: int, seed: int = None) -> int:
    a = 39177369995579819498972128804676596941198511312402174107900118507767888787985319889078498768125726538781142699985438519849879849879867913387985078149715117956575598705232859627482107678765877225323948753141
    c = 0
    num = seed or 1
    while True:
        num = (a * num + c) % m
        yield num


def xorshift32(seed: int, n: int) -> int:
    xor_parts = list()

    while n != 0:
        x = seed & 0x7fffffff  # 32 bits
        x ^= x << 13
        x ^= x >> 17
        x ^= x << 5
        x = x & 0x7fffffff  # 32 bits novamente
        xor_parts.append(x)

        n >>= 32

    x = 0
    for i, part in enumerate(xor_parts):
        x |= part << (32 * i)

    return x


def miller_rabin(n: int, k: int) -> bool:
    if n == 2:
        return True

    if n % 2 == 0:
        return False

    r, s = 0, n - 1
    while s % 2 == 0:
        r += 1
        s //= 2
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, s, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


def fermat_little_theorem(n: int) -> bool:
    return (2 << (n - 2)) % n == 1


def measure_time(f):
    n = 100000
    start = time.time()
    for _ in range(n):
        f()
    end = time.time()
    time_ = (end - start) / n

    print(time_)


if __name__ == "__main__":
    for length in BITS_LENGTH:
        print(f"LCG {length}")
        measure_time(lambda: lcg(m=length, seed=2**length-1))
        print(f"Xorshift {length}")
        measure_time(lambda: xorshift32(n=length, seed=1))
        x = False
        generator = lcg(m=2**length, seed=2**length-1)
        start = time.time()
        while(not x):
            x = miller_rabin(next(generator), 40)
        end = time.time()
        print(f"{length} :  {(end - start)}")
