n = int(input())
count_a = 0
count_b = 0
count_c = 0
for i in range(n):
    a = int(input())
    if a % 2 != 0:
        count_a += 1
    if a % 3 == 0 and a % 5 != 0:
        count_b += 1
    if (i + 1) % 2 == 0 and a % 2 != 0:
        count_c += 1
print(count_a)
print(count_b)
print(count_c)