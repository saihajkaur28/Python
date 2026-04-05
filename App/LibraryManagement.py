import streamlit as st
from datetime import date, timedelta

# ------------------ DATA (SIMULATION DATABASE) ------------------

books = {
    "B101": {"title": "Python Basics", "genre": "Technology", "available": 3},
    "B102": {"title": "Data Structures", "genre": "Technology", "available": 2},
    "B103": {"title": "Harry Potter", "genre": "Fiction", "available": 1},
    "B104": {"title": "Atomic Habits", "genre": "Self Help", "available": 2},
}

users = {
    "S101": {"name": "Student A", "role": "Student", "issued": {}, "fine": 0},
    "T201": {"name": "Teacher B", "role": "Teacher", "issued": {}, "fine": 0},
}

ADMIN_ID = "admin"

# ------------------ SESSION STATE ------------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_id = None
    st.session_state.role = None

# ------------------ FUNCTIONS ------------------

def calculate_fine(issue_date):
    days_late = (date.today() - issue_date).days - 7
    if days_late > 0:
        return days_late * 5
    return 0

def recommend_books(genre):
    return [b["title"] for b in books.values() if b["genre"] == genre]

def logout():
    st.session_state.logged_in = False
    st.session_state.user_id = None
    st.session_state.role = None
    st.rerun()

# ------------------ APP TITLE ------------------

st.title("📚 Smart Library Management System")

# ------------------ LOGIN PAGE ------------------

if not st.session_state.logged_in:
    st.subheader("Login")

    role = st.selectbox("Login as", ["Librarian", "Student", "Teacher"])
    user_id = st.text_input("Enter User ID")

    if st.button("Login"):
        if role == "Librarian" and user_id == ADMIN_ID:
            st.session_state.logged_in = True
            st.session_state.role = "Admin"
            st.session_state.user_id = user_id
            st.success("Logged in as Librarian")
            st.rerun()

        elif user_id in users and users[user_id]["role"] == role:
            st.session_state.logged_in = True
            st.session_state.role = role
            st.session_state.user_id = user_id
            st.success(f"Logged in as {role}")
            st.rerun()

        else:
            st.error("Invalid ID or Role")

# ------------------ ADMIN DASHBOARD ------------------

elif st.session_state.logged_in and st.session_state.role == "Admin":
    st.header("👩‍💼 Librarian Dashboard")

    # Inventory
    st.subheader("📖 Book Inventory")
    for code, book in books.items():
        st.write(code, book)

    # Issued Books Report
    st.subheader("📋 Issued Books Report")

    issued_found = False
    total_issued = 0

    for uid, user in users.items():
        if user["issued"]:
            issued_found = True
            st.markdown(f"### 👤 {user['name']} ({user['role']}) | ID: {uid}")

            user_fine_preview = 0

            for bc, issue_date in user["issued"].items():
                total_issued += 1
                due_date = issue_date + timedelta(days=7)
                days_left = (due_date - date.today()).days

                if days_left < 0:
                    overdue_days = -days_left
                    fine = overdue_days * 5
                    user_fine_preview += fine
                    st.error(
                        f"📕 {bc} | Issued: {issue_date} | Due: {due_date} | "
                        f"OVERDUE by {overdue_days} days | Expected Fine ₹{fine}"
                    )

                elif days_left <= 2:
                    st.warning(
                        f"📘 {bc} | Issued: {issue_date} | Due: {due_date} | "
                        f"{days_left} day(s) left"
                    )

                else:
                    st.success(
                        f"📗 {bc} | Issued: {issue_date} | Due: {due_date} | "
                        f"{days_left} days remaining"
                    )

            if user_fine_preview > 0:
                st.markdown(f"💰 **Expected Fine: ₹{user_fine_preview}**")

    if not issued_found:
        st.info("No books are currently issued")

    st.divider()
    st.markdown(f"📊 **Total Issued Books: {total_issued}**")

    # Update Quantity
    st.subheader("➕ Update Book Quantity")
    book_code = st.text_input("Enter Book Barcode")
    quantity = st.number_input("Increase / Decrease Quantity", step=1)

    if st.button("Update Book"):
        if book_code not in books:
            st.error("Invalid book barcode")
        elif books[book_code]["available"] + quantity < 0:
            st.error("Quantity cannot be negative")
        else:
            books[book_code]["available"] += quantity
            st.success("Book quantity updated successfully")

    if st.button("Logout"):
        logout()

# ------------------ USER DASHBOARD ------------------

elif st.session_state.logged_in and st.session_state.role in ["Student", "Teacher"]:
    user = users[st.session_state.user_id]

    st.header(f"👤 Welcome {user['name']} ({user['role']})")

    # Issued Books
    st.subheader("📘 Your Issued Books")
    if user["issued"]:
        for bc, issue_date in user["issued"].items():
            due_date = issue_date + timedelta(days=7)
            days_left = (due_date - date.today()).days

            if days_left < 0:
                st.error(
                    f"📕 {bc} | Issued: {issue_date} | Due: {due_date} | "
                    f"OVERDUE by {-days_left} days"
                )
            elif days_left <= 2:
                st.warning(
                    f"📘 {bc} | Issued: {issue_date} | Due: {due_date} | "
                    f"Hurry! {days_left} day(s) left"
                )
            else:
                st.success(
                    f"📗 {bc} | Issued: {issue_date} | Due: {due_date} | "
                    f"{days_left} days remaining"
                )
    else:
        st.info("No books issued")

    # Issue Book
    st.subheader("📤 Issue Book")
    issue_code = st.text_input("Enter Book Barcode to Issue")

    if st.button("Issue Book"):
        if issue_code in books and books[issue_code]["available"] > 0:
            books[issue_code]["available"] -= 1
            user["issued"][issue_code] = date.today()
            st.success("Book issued successfully")
        else:
            st.error("Book not available or invalid barcode")

    # Return Book
    st.subheader("📥 Return Book")
    return_code = st.text_input("Enter Book Barcode to Return")

    if st.button("Return Book"):
        if return_code in user["issued"]:
            fine = calculate_fine(user["issued"][return_code])
            user["fine"] += fine
            del user["issued"][return_code]
            books[return_code]["available"] += 1
            st.success(f"Book returned. Fine charged ₹{fine}")
        else:
            st.error("This book is not issued to you")

    # Fine
    st.subheader("💰 Total Fine")
    st.write(f"₹ {user['fine']}")

    # Recommendations
    st.subheader("📚 Book Recommendations")
    genre = st.selectbox("Choose Genre", ["Technology", "Fiction", "Self Help"])

    if st.button("Get Recommendations"):
        recs = recommend_books(genre)
        if recs:
            st.write(recs)
        else:
            st.info("No books found in this genre")

    if st.button("Logout"):
        logout()
