expenses = []  #list to store expenses in form of dictionaries

print("Welcome to Expense Tracker!")
monthly_budget = int(input("Enter your Monthly Budget: "))

while True:
    print("\nMAIN MENU:")
    print("1. Add Expense")
    print("2. View Expenses")
    print("3. View Total expenses")
    print("4. Category-wise Monthly Expense Summary")
    print("5. Exit")

    choice = input("Enter your Choice: ")

#ADD EXPENSE
    if choice == "1":
        date = input("Enter the date of expense (DD-MM-YY):")
        amount = float(input("Enter the expense amount: "))
        category = input("Enter the expense category (eg. Food, Shopping etc.): ")
        description = input("enter a brief description about the category: ")

        expense = {
            "date": date,
            "amount": amount,
            "category": category,
            "description": description        }
        expenses.append(expense)
        print("\nExpense added successfully!")

#MONTHLY BUDGET CHECK
        month_year = date[3:]  #extract month and year from date
        monthly_total = 0
        for e in expenses:
            if e['date'][3:] == month_year:
                monthly_total += e['amount']

        if monthly_total > monthly_budget:
            print("⚠️ YOU HAVE EXCEEDED YOUR MONTHLY BUDGET!")   
            print(f"Total Expense this Month: {monthly_total}, Monthly Budget: {monthly_budget}") 

#VIEW EXPENSES
    elif choice == "2":
        if not expenses:   #if expenses list is empty
            print("\nNo expenses recorded yet.")
        else:
            print("\nRecorded Expenses:")
            count = 1
            for i in expenses:
                print(f"Expense {count}:"
                      f"\nDate: {i['date']}\nAmount: {i['amount']}\nCategory: {i['category']}\nDescription: {i['description']}")
                count+=1

#VIEW TOTAL EXPENSES
    elif choice == "3":
        total = sum(x['amount'] for x in expenses)
        print(f"\nTotal Expenses: {total}")  

#CATEGORY-WISE MONTHLY SUMMARY
    elif choice == "4":
        month = input("Enter the month and year for summary (MM-YY): ")
        category_summary = {}

        for e in expenses:
            if e['date'][3:] == month:  #check if month and year match
                cat = e['category']    #get category of expense
                category_summary[cat] = category_summary.get(cat, 0) + e['amount']    #get - if cat not in dict, then 0 else get value of cat and add amount
        
        if not category_summary:   #if no expenses found for that month
            print(f"\nNo Expenses Recorded for {month}.")

        else:
            print(f"\nCategory-wise Expense Summary for {month}:")
            for cat, amt in category_summary.items():
                print(f"{cat} : {amt}")

#EXIT
    elif choice == "5":
        print("Thank you for using Expense Tracker. Goodbye!👋")
        break

    else:
        print("Invalid choice. Please select a valid option (1-4).")
        


