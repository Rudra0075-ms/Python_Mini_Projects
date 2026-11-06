bal = 10000.0

while True:
    print("\n1.Deposit 2.Withdraw 3.Balance 4.Exit")
    ch = input("Choice: ")
    
    if ch == '1':
        amt = float(input("Amount: "))
        bal += amt
    elif ch == '2':
        amt = float(input("Amount: "))
        if amt > bal: print("Insufficient balance!")
        else: bal -= amt
    elif ch == '3':
        print(f"Balance: {bal}")
    elif ch == '4':
        print("Goodbye!")
        break
    else:
        print("Invalid Choice")

