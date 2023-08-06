def factorial(n):
    if n == 0: return 1
    else: return n * factorial(n - 1)

def double_factorial(n):
    if n == 0: return 1
    else: return n * double_factorial(n - 2)

def subfactorial(n):
    return round(factorial(n) / 2.718)

def primorial(n):

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

    if n == 1: return 1
    elif isprime(n): return n * primorial(n - 1)
    else: return primorial(n - 1)

def p_primorial(n):

    def p(n):
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
        return result[-1]

    return primorial(p(n))

def superfactorial(n):
    if n == 0: return 1
    else: return factorial(n) * superfactorial(n - 1)

def superduperfactorial(n):
    if n == 0: return 1
    else: return superfactorial(n) * superduperfactorial(n - 1)