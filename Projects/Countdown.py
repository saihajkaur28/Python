#Countdown Timer(With one second gap)

import time

msg = input("What's the Occasion: ")
count = int(input("Enter time in seconds : "))

print("\nCountdown Starts now")
for i in range(count,0,-1):
    print(i)
    time.sleep(1)

print("WOOHOOO!",msg)   