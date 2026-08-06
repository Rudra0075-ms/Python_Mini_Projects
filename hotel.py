f = int(input("Floors: "))
r = int(input("Rooms per floor: "))

hotel = []

for i in range(f):
    row = []
    for j in range(r):
        row.append(input("A/B: ").upper())
    hotel.append(row)

print("\nRoom Chart")
for i in hotel:
    print(*i)
