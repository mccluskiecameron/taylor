from math import factorial as fac

def partitions(n, I=1):
    """The integer partitions
    All possible ordered lists of positive numbers summing to n.
    borrowed from: https://stackoverflow.com/a/44209393/4455114
    """
    yield (n,)
    for i in range(I, n//2 + 1):
        for p in partitions(n-i, i):
            yield (i,) + p

def partcounts(n, I=1):
    """Yields a list where each index i contains the number of appearances of i
    in the respective term above.
    """
    yield [0]*(n-1) + [1]
    for i in range(I, n//2+1):
        for p in partcounts(n-i, i):
            p += [0]*(i)
            p[i-1]+=1
            yield p

def faadibruno(f, g):
    """Faà di Bruno's formula:
    Evaluate the nth derivative if f(g(x))
    rakes a list f with the nth term being the nth derivative of f evaluated at
    g(x), and a list g with the nth term being the nth term being the nth
    derivative evaluated at x. Both should start with the first derivative.
    """
    for n in range(1, len(f)+1):
        S = 0
        for p in partcounts(n):
            P = fac(n) * f[sum(p)-1]
            for i in range(len(p)):
                P *= g[i]**p[i] / fac(p[i]) / fac(1+i)**p[i]
            S += P
        yield S

def tayparts(n):
    """Same as partcounts, but without the (n,) term"""
    for i in range(1, 1+n//2):
        for p in partcounts(n-i, i):
            p += [0]*(i-1)
            p[i-1]+=1
            yield p

def _taylor_inverse(f):
    """The inverse of a taylor series
    Taking faà di brunno's formula, we solve for the nth derivative of g at x
    for each n. f should be the first n derivatives of f, evaluated at g(x).
    """
    g = [1/f[0]]
    for n in range(2, 1+len(f)):
        S = 0
        for p in tayparts(n):
            P = fac(n) * f[sum(p)-1]
            for i in range(len(p)):
                P *= g[i]**p[i] / fac(p[i]) / fac(i+1)**p[i]
            S += P
        g.append(-S/f[0])
    return g

def it_choose(n, k):
    f = 1
    for i in range(k+1, n+1):
        yield f
        f *= i
        f //= (i - k)
    yield f

def taylor_recenter(x, c, t):
    """given a taylor series centered at c, return a taylor series centered at x.
    The result will give identical results, having only a different center.
    """
    n=len(t)
    for k in range(n):
        S=0
        P=1
        for i in range(k+1, n):
            S+=t[i-1]*P
            P*=i*(x-c)/(i-k)
        S+=t[-1]*P
        yield S

def taylor_inverse(t):
    """given the first n terms of a taylor series centered at 0, returns the
    first n terms of the inverse taylor series also centered at 0.
    """
    derivs = [a*fac(i) for i, a in enumerate(t[1:])]
    g = _taylor_inverse(derivs)
    G = [0]+[a/fac(i) for i, a in enumerate(g)]
    F = list(taylor_recenter(0, derivs[0], G))
    return F

def taylor(x, c, t):
    S = 0
    for i in reversed(t):
        S *= x-c
        S += i
    return S

if __name__ == "__main__":
    """f=exp, g=ln. f(g(x)) = x. should print [1, 0, 0, ...]"""
    print(list(faadibruno([1, 1, 1, 1, 1, 1, 1], [1, -1, 2, -6, 24, -120, 720])))

    """f=ln, g=exp. should print [1, 1, 1, ...]. 
    Note that the ln taylor series centered at one is defined over (0,2], and yet
    the inverse is defined over the reals"""
    print(list(_taylor_inverse([1, -1, 2, -6, 24, -120, 720])))

    """f=exp, t=ln, c=0. should print ln 1 = 0"""
    t = taylor_inverse([1/fac(n) for n in range(15)])
    print(round(taylor(1, 0, t), 10))

