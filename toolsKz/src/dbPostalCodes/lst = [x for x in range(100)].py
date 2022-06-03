lst = [x for x in range(100)]
print(lst[20:80])



a = "alex"
print(a[-2:])


import sys

from django.conf import settings

a = [1, 2, "a"]
b = [1, 2, "a"]

sys.getsizeof(a)
print(

    sys.getsizeof(a),
    sys.getsizeof(b),
)


class A:

    def print_g():
        print("a")
product = A.print_g()

print(0 % 2 == 0)


param = 0


for param in range(-100, 100):
    try:
        any([x/y for y in range(x, 100) if  y % 2 == 0] for x in range(abs(param), 10) )
    except:
        print(param)