import random

l = '0123456789ABCDEF'
for i in range(64):
	number = ""
	for j in range(8):
		number += l[random.randint(0,15)]
	print(number, end=",\n")