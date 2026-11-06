n = int(input("No. of employees: "))
t = 0

for i in range(n):
    id = input("Emp ID: ")
    name = input("Name: ")
    b = float(input("Basic Salary: "))

    h = b * 0.20
    d = b * 0.15
    p = b * 0.12
    g = b + h + d
    net = g - p

    print("Gross =", g)
    print("Net =", net)

    if net > 80000:
        print("Grade A")
    elif net >= 60000:
        print("Grade B")
    elif net >= 40000:
        print("Grade C")
    else:
        print("Grade D")

    t += net

print("Total Employees =", n)
print("Average Salary =", t / n)

