n = int(input("No. of students: "))

p = f = 0
high = 0

for i in range(n):
    name = input("Name: ")
    total = 0
    pass1 = True

    for j in range(5):
        m = int(input("Marks: "))
        total += m
        if m < 40:
            pass1 = False

    per = total / 5

    if per >= 90:
        g = "A+"
    elif per >= 80:
        g = "A"
    elif per >= 70:
        g = "B"
    elif per >= 60:
        g = "C"
    elif per >= 50:
        g = "D"
    else:
        g = "Fail"

    print(name, total, per, g)

    if pass1:
        print("PASS")
        p += 1
    else:
        print("FAIL")
        f += 1

    if per > high:
        high = per

print("Passed =", p)
print("Failed =", f)
print("Highest % =", high)

  