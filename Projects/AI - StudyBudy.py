#Rule-Bases Chatbot

import datetime as dt
import time

time = dt.datetime.now().hour
user = input("enter your name :")

if 5<= time <12:
    print("Good Morning", user)
elif 12<= time <17:
    print("Good Afternoon", user)
elif 17<= time <=20:
    print("Good Evening", user)
else:
    print("Good Night", user)

print("Welcome to your Chatbot")
name = input("What would you like to call me:")
print("Hi I'm", name)
print("You can ask me any question and type 'bye' to exit")

responses = {
    "hello" : "Hi, Welcome. How can I help you?",
    "how are you" : "I'm fine. Thank You!"
    }
