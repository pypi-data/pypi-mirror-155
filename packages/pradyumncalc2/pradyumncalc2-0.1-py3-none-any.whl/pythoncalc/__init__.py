def add(a,b):
    return a+b

def sub(a,b):
    return a-b

def mul(a,b):
    return a*b

def div(a,b):
    return a/b

def si(p,t,r):
    return p*t*r/100

def ci(p, r, t):
    x = p * (pow((1 + r / 100), t)) 
    return x 