import random 
  

#BASIC   
n = random.randint(1,10)
guess = None

while guess != n:   #for i in range(1,n+1):
    guess = int(input("Guess a number between 1 and 10: "))
    if guess < n:
        print("Too low! Try again.")
    elif guess > n:
        print("Too high! Try again.")
    else:
        print("Congratulations! You guessed the correct number.")





