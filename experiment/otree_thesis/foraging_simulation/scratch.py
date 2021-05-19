import random
vec =[]
for i in range(10**7):
    vec.append(random.gauss(0,0.1))

print(max(vec))
print(min(vec))