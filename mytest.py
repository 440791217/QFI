import random

faults=[5,4,2,6,7,8,10]

print(random.sample(faults,1))
num=0x00
print(num)
num ^= (1 << 3)
print(num)
print(hex(num))
# print()