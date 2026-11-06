while True:
    units = int(input("Enter units: "))

    if units <= 100:
        bill = units * 2
    elif units <= 200:
        bill = 200 + (units - 100) * 3
    elif units <= 400:
        bill = 500 + (units - 200) * 5
    else:
        bill = 1500 + (units - 400) * 7

    print("Bill =", bill)
    print("GST =", bill * 0.10)
    print("Total =", bill * 1.10)

    if input("More? (y/n): ") != "y":
        break
    
