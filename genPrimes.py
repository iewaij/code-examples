def genPrimes_better():
    primes = []   # primes generated so far
    last = 1      # last number tried
    while True:
        last += 1
        for p in primes:
            if last % p == 0:
                break
        else:
            primes.append(last)
            yield last

def genPrimes():
    prime_list = [2]
    yield 2
    prime_next = 3
    while True:
        isPrime = True
        for prime in prime_list: 
            if prime_next % prime == 0:
                isPrime = False
        if isPrime == True:
            yield prime_next
            prime_list.append(prime_next)
        prime_next += 1
        

pri = genPrimes()
print(pri.__next__())
print(pri.__next__())