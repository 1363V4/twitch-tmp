# from PIL import Image
# from pathlib import Path


# cwd = Path.cwd()
# im = Image.open(cwd / "static/img" / "stario.png")
# print(im.size)

# smol = im.resize((32, 32))
# print(smol.size)
# smol.save(cwd / "smol.png")

from array import array
from uuid import uuid4

from faker import Faker

fake = Faker()
u1 = str(uuid4())
u2 = uuid4().hex

# test = array("w")
# print(test)
# test.extend(fake.name())
# print(test)
# print(test[0])
# print(test[1])
# test.clear()
# test.extend(u1)
# print(test)
# test.clear()
# test.extend(u2)
# print(test)
# i'd like multiple str in here... do i have to preallocate?

# test = array("w", " " * 32)
# print(test)
# for n, char in enumerate(fake.name()):
#     test[n] = char
# print(test)
# # yeah it kind of works that way
# for n, char in enumerate(u2):
#     test[n] = char
# print(test)
# # like a glove!
# #
# # i wonder if there's a smarter way to write it
# # not using string lol dummy
# # u3 = uuid4().hex  # 32 char > 16 octets
# # u3 = uuid4().urn  # ??? ah ok ce truc de con
# # print(u3)
# # u3 = uuid4().bytes  # 16 byte
u3 = uuid4()
# print(u3.hex)
# print(u3.bytes)
u3 = u3.bytes
test = array("B", u3)
# # test.frombytes(u3)
print(test)
test = array("H")
test.frombytes(u3)
print(test)
test = array("I")
test.frombytes(u3)
print(test)
test = array("L")
test.frombytes(u3)
print(test)
# u4 = uuid4().int
# print(u4)

# 32bytes>
# int to enum?
#
# from enum import Enum


# class Name(Enum):
#     USER1 = fake.name()


# print(Name.USER1.value)
# Name.USER2 = "watji" non il aime pas
# ...
# on peut laisser en liste ?
# comme ça c'st évident ?
#
# from pprint import pprint
#
# NAMES = [fake.name() for _ in range(10)]
# pprint(NAMES)
# print(NAMES[0])
#
# print(int("c7", 16))
# print(int("f0", 16))
# print(int("d8", 16))
# print(int("43", 16))
# print(int("52", 16))
# print(int("3d", 16))

# import array
#
# for t in array.typecodes + "bB":
#     a = array.array(t, [])
#     print(a, a.itemsize)
