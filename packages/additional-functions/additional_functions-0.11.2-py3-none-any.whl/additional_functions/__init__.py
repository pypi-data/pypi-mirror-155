def isprime(n):
    result = []
    d = 2
    while d * d <= n:
        if n % d == 0:
            result.append(d)
            n //= d
        else:
            d += 1
    if n > 1:
        result.append(n)
    if len(result) > 1: return False
    else: return True

def n_primes(n):
    result = []
    i = 0
    m = 1
    while i < n:
        m += 1
        k = True
        for j in result:
            if m % j == 0:
                k = False
                break
        if k:
            result.append(m)
            i += 1
    return result

def prime_factors(a):
    result = []
    d = 2
    while d * d <= a:
        if a % d == 0:
            result.append(d)
            a //= d
        else:
            d += 1
    if a > 1:
        result.append(a)
    return result

def fibo(n):
    if n <= 1:
        return n
    else:
        return fibo(n - 1) + fibo(n - 2)

def gcd(a, b):
    while a != 0 and b != 0:
        if a > b:
            a = a % b
        else:
            b = b % a
    return a + b

def lcm(a, b):
    return int((a * b) / gcd(a, b))