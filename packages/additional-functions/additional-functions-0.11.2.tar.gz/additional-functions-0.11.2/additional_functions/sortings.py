def bubble(a):
    k = 0
    while k < len(a) - 1:
        k = 0
        for j in range(0, len(a)-1):
            if a[j] > a[j+1]:
                a[j] = a[j] + a[j+1]
                a[j+1] = a[j] - a[j+1]
                a[j] = a[j] - a[j+1]
            else:
                k += 1
    return a

def insertion(a):
    for j in range(1, len(a)):
        key = a[j]
        i = j - 1
        while i >= 0 and a[i] > key:
            a[i+1] = a[i]
            i -= 1
        a[i+1] = key
    return a

def merge(a):

    def sort(array, m):
        mass = []
        for i in range(0, m):
            mass.append(array[i])
        if m <= 1:
            array[0] = mass[0]
        else:
            l = []
            r = []
            for i in range(0, m):
                if i < int(m/2):
                    l.append(mass[i])
                else:
                    r.append(mass[i])
            sort(l, len(l))
            sort(r, len(r))
            h = 0
            f = 0
            c = []
            while h < len(l) and f < len(r):
                if l[h] < r[f]:
                    c.append(l[h])
                    h += 1
                else:
                    c.append(r[f])
                    f += 1
            while h < len(l):
                c.append(l[h])
                h += 1
            while f < len(r):
                c.append(r[f])
                f += 1
            for i in range(0, m):
                array[i] = c[i]

    sort(a, len(a))
    return a

def quick(a):

    def sort(array, b, e):
        l = b
        r = e
        p = array[int((l + r) / 2)]
        while l <= r:
            while array[l] < p:
                l += 1
            while array[r] > p:
                r -= 1
            if l <= r:
                if l < r:
                    array[l] = array[l] + array[r]
                    array[r] = array[l] - array[r]
                    array[l] = array[l] - array[r]
                l += 1
                r -= 1
        if b < r:
            sort(array, b, r)
        if e > l:
            sort(array, l, e)
    
    sort(a, 0, len(a) - 1)
    return a

def selection(a):
    for i in range(0, len(a) - 1):
        imin = i
        for j in range(i + 1, len(a)):
            if a[j] < a[imin]:
                imin = j
        if imin != i:
            a[i] = a[i] + a[imin]
            a[imin] = a[i] - a[imin]
            a[i] = a[i] - a[imin]
    return a