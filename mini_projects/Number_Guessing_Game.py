import random
n=random.randint(1,10)
guess=int(input("guess a number="))  #5
if guess==n:
    print("You Win!")
else:
    print("Try Again!") 