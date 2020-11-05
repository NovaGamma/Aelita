from variable import*
from second import test

def main(v):
    if v > 0:
        Muted.append(v)
    else:
        test(v)


v = int(input())
while v != 0:
    main(v)
    print(Muted)
    v = int(input())
