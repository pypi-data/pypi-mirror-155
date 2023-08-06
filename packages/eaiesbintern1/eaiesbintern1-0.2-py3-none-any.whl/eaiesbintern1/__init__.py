def ADD(n,n1):
    return n+n1

def SUB(n,n1):
    return n-n1

def MUL(n,n1):
    return n*n1

def DIV(n,n1):
    return n/n1

def SI(P,R,T):
    return (P*R*T)/100

def CI(P,R,T):
    ci= P * (pow(( 1 + R / 100),T))
    return ci