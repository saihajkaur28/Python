import time
import random

score = 0
round_scores=[]

print("🎮 Welcome to the Number Guessing Game!!")

while True:

    print("\nMAIN MENU:")
    print("1. New Game (Reset Score)")
    print("2. Continue Game")
    print("3. View Score")
    print("4. Exit")

    menu_choice = input("Enter your choice: ")

    if menu_choice == '1':
        score = 0
        round_scores.clear()
        print("\nStarting a New Game! Your score has been reset.")

    elif menu_choice == '2':
        print("▶️ Continue Game")

    elif menu_choice == '3':
        if not round_scores:
            print("\nNo rounds played yet.")
        else:
            print("\nSCOREBOARD 📊")
            for i, rs in enumerate(round_scores, 1):
                print(f"Round {i} : {rs} points")
            print(f"Total Score : {score}")
            continue 

    elif menu_choice == '4':
        print("Exiting the game. Thanks for playing! 👋")
        break

    else:
        print("Invalid choice. Please select a valid option (1-4).")
        continue

    #Difficulty Selection

    print("\nSelect Difficulty Level:")

    print("1. Easy (Number between 1-10, 5 attempts)")
    print("2. Medium (Number between 1-50, 7 attempts)")
    print("3. Hard (Number between 1-100, 10 attempts)")

    difficulty = input("Enter your choice : ")

    if difficulty == '1':
        max_num = 10
        attempts = 5

    elif difficulty == '2':
        max_num = 50
        attempts = 7

    elif difficulty == '3':
        max_num = 100
        attempts = 10

    else:
        print("Invalid choice. Please select a valid option (1-3).")
        continue

    #GAME STARTS

    sec_num = random.randint(1, max_num) 
    hint_used = False
    start_time = time.time()

    print(f"\nI have choosen a number beteween 1 and {max_num}.\nYou have {attempts} attempts to guess it.\n\tGOOD LUCK! 🍀")   

    for i in range (1, attempts+1):
        guess = int(input(f"Attempt {i}/{attempts} "))

        if guess == sec_num:
            end_time = time.time()
            time_taken = round(end_time - start_time , 2)
            print(f"🎉 CONGRATULATIONS! You guessed the Correct Number {sec_num} in {i} attempts and {time_taken} seconds.")

            round_score = 1
            if hint_used :
                round_score -= 0.5
        
            score += round_score
            round_scores.append(round_score)
            break

        print("❌ Incorrect guess.")

        want_hint = input("Do you want a hint? (yes/no): ").lower()
        if want_hint == 'yes':
            hint_used = True
            diff = abs(sec_num - guess)
                    
            if diff > max_num // 2:
                print("🥶 Very Cold! Very Far")  
            elif diff > max_num // 4:
                print("❄️ Cold! Far")      
            elif diff > max_num // 10:
                print("🌤️ Warm! Close")    
            else:
                print("🔥 Hot! Very Close")     

    else:
        print(f"😞 GAME OVER! You've used all your attempts. The correct number was {sec_num}.")
        round_scores.append(0)

    print(f"Your Current Total Score is: {score} Points.")

    play_again = input("Do you want to play again? (yes/no): ").lower()
    if play_again != 'yes':
        print("Exiting the game. Thanks for playing! 👋")
        break

    




      
