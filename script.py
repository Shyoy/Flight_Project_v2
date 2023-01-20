from random import choice
from string import ascii_letters, digits, punctuation
from itertools import count

keys = digits + ascii_letters + punctuation

counter = count()
output = []
while len(output) < 90:
    next(counter)
    key = choice(keys)
    if output.count(key) < 2:
        output += key 

print(len(output))
print("Amount of time looped:",counter )
print("".join(output))