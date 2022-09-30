import random

def rabinMiller(n, d):
    a = random.randint(2, (n - 2) - 2)
    x = pow(a, int(d), n)
    if x == 1 or x == n - 1:
        return True

    #pierwiastkuj dopóki d != n - 1
    while d != n - 1:
        x = pow(x, 2, n)
        d *= 2

        if x == 1:
            return False
        elif x == n - 1:
            return True
    
    #nie jest pierwsza
    return False

def isPrime(n):
    #zwróć True jeśli n jest pierwsze, jeśli nie pewne, wykonaj test Rabina-Millera 128 razy

    #pominięcie 0 i 1
    if n < 2:
        return False

    #małe liczby pierwsze do zaoszczędzenia czasu
    lowPrimes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997]

    #jeśli liczba jest w tablicy małych liczb pierwszych
    if n in lowPrimes:
        return True

    #jeśli liczba jest podzielna przez liczbę pierwszą z tablicy, nie jest pierwsza
    for prime in lowPrimes:
        if n % prime == 0:
            return False
    
    #znajdź c, które: c * 2 ^ r = n - 1
    c = n - 1 #c jest parzyste, ponieważ nie podzieliło się przez 2, które jest w tablicy 
    while c % 2 == 0:
        c /= 2 #zamiana c na nieparzyste

    #wykonaj test Rabina-Millera 128 razy, wykonywany określoną ilość razy, ponieważ jest testem probabilistycznym, stosującym liczby losowe
    for i in range(128):
        if not rabinMiller(n, c):
            return False

    return True

def generateKeys(keysize=1024):
    e = d = N = 0

    #wygeneruj dwie liczby pierwsze zależne od keysize
    p = generateLargePrime(keysize)
    q = generateLargePrime(keysize)

    print(f"p: {p}")
    print(f"q: {q}")

    N = p * q #moduł RSA
    phiN = (p - 1) * (q - 1) # tocjent

    #wybierz e, które jest relatywnie pierwsze oraz 1 < e <= tocjent
    while True:
        e = random.randrange(2 ** (keysize - 1), 2 ** keysize - 1)
        if (isCoPrime(e, phiN)):
            break

    #wybierz d, które jest odwrotnością modulo e i zależne od tocjentu, e * d (mod tocjent) = 1
    d = modularInv(e, phiN)

    return e, d, N

def generateLargePrime(keysize):
    #zwróć liczbę pierwszą, która jest podniesiona do potęgi keysize
    while True:
        num = random.randrange(2 ** (keysize - 1), 2 ** keysize - 1)
        if (isPrime(num)):
            return num

def isCoPrime(p, q):
    #zwróć True jeśli NWD  p i q jest jeden, tzn. że liczby są relatywnie pierwsze
    return gcd(p, q) == 1

def gcd(p, q):
   #algorytm Euklidesa do znalezienia NWD p i q
    while q:
        p, q = q, p % q
    return p

def egcd(a, b):
    s = 0; old_s = 1
    t = 1; old_t = 0
    r = b; old_r = a
    
    while r != 0:
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        old_s, s = s, old_s - quotient * s
        old_t, t = t, old_t - quotient * t

    #zwróć NWD, x, y
    return old_r, old_s, old_t

def modularInv(a, b):
    gcd, x, y = egcd(a, b)

    if x < 0:
        x += b

    return x

def encrypt(e, N, msg):
    cipher = ""

    for c in msg:
        m = ord(c)
        cipher += str(pow(m, e, N)) + " "

    return cipher

def decrypt(d, N, cipher):
    msg = ""

    parts = cipher.split()
    for part in parts:
        if part:
            c = int(part)
            msg += chr(pow(c, d, N))

    return msg

def main():
    keysize = 32

    e, d, N = generateKeys(keysize)

    msg = "So Long, and Thanks for All the Fish"

    enc = encrypt(e, N, msg)
    dec = decrypt(d, N, enc)

    print(f"Message: {msg}")
    #Klucz publiczny
    print(f"e: {e}")
    f = open("public_key.key", "w")
    f.write(str(e))
    f.close()

    #Klucz prywatny
    print(f"d: {d}")
    f = open("private_key.key", "w")
    f.write(str(d))
    f.close()

    print(f"N: {N}")

    #Wiadomość zakodowana
    print(f"enc: {enc}")
    f = open("enc.msg", "w")
    f.write(enc)
    f.close()

    #Wiadomość zdekodowana
    f = open("msg.msg", "w")
    f.write(dec)
    f.close()
    print(f"dec: {dec}")

main()