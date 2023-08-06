import math
print('Hello World! (if you see this then this work)')

def tti(n):
    if round(n) == n:
        return round(n)
    else:
        return n

def avg(numbers: list):
    return tti(sum(numbers) / len(numbers))


def pt(k1,k2,mode="h"):
    if mode=="h":
        return tti(math.sqrt(k1 ** 2 + k2 ** 2))
    else:
        if k1 > k2:
            return tti(math.sqrt(k1** 2 - k2 ** 2))
        else:
            return tti(math.sqrt(k2 ** 2 - k1 ** 2))
        
