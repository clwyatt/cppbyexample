from itertools import izip_longest

def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), ... , (sn-1,sn)"
    a = iter(iterable)
    b = iter(iterable[1:])
    return izip_longest(a, b, fillvalue=None)

if __name__ == "__main__":

    L = ['a', 'b', 'c', 'd']

    for x,y in pairwise(L):
        print x,y
