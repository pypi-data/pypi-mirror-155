def add(a,b):
    return a+b

def sub(a,b):
    return a-b

def mul(a,b):
    return a*b

def div(a,b):
    return a/b

def power(num,exp):
    p = 1
    i = 1
    while(i <= exp):
        p = p * num
        i = i + 1
    return p

def rem(a,b):
    return a%b
def isOdd(a):
    return((a % 2) != 0)

def isEven(a):
    return((a % 2) == 0)

def fib(a):
    if a == 0:
        return 0
    elif a == 1 or a== 2:
        return 1
    else:
        return fib(a-1) + fib(a-2)
        
def concat(a,b):
    return(str(a)+str(b))


