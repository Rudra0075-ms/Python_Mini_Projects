while True:
    u = int(input("Enter units: "))

    if u <= 100:
        bill = u * 2
    elif u <= 200:
        bill = 200 + (u - 100) * 3
    elif u <= 400:
        bill = 500 + (u - 200) * 5
    else:
        bill = 1500 + (u - 400) * 7

    print("Bill =", bill)
    print("GST =", bill * 0.10)
    print("Total =", bill * 1.10)

    if input("More? (y/n): ") != "y":
        break
    
