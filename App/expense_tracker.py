import streamlit as st
import pandas as pd

st.set_page_config(page_title="💸 Expense Tracker", page_icon="💸", layout="centered")

# ================= ALERT DIALOG =================
@st.dialog("🚨 Alert")
def alert_dialog():
    st.write("⚠️ Monthly expense limit exceeded!")
    st.write("Please review your spending.")

# ================= SESSION STATE INIT =================
if "expenses" not in st.session_state:
    st.session_state.expenses = []

if "budget_alert_shown" not in st.session_state:
    st.session_state.budget_alert_shown = False

if "update_success" not in st.session_state:
    st.session_state.update_success = False

if "delete_success" not in st.session_state:
    st.session_state.delete_success = False

# ================= TITLE =================
st.title("💸 Expense Tracker Application")
st.subheader("Track and Manage Your Expenses Easily")

# ================= MONTHLY BUDGET =================
monthly_budget = st.number_input(
    "Set Your Monthly Budget:",
    min_value=0,
    step=500,
    value=5000
)

# ================= ADD EXPENSE =================
st.header("➕ Add Expense")

with st.form("Expense Form"):
    date = st.date_input("Date of Expense:")
    amount = st.number_input("Amount:", min_value=0.0, step=100.0)
    category = st.text_input("Category (eg. Food, Shopping, Travel etc.):")
    description = st.text_area("Brief Description:")

    submit = st.form_submit_button("Add Expense")

    if submit:
        if category and date and amount > 0:
            st.session_state.expenses.append({
                "Date": date,
                "Amount": amount,
                "Category": category,
                "Description": description
            })
            st.success("✅ Expense Added Successfully!")
        else:
            st.error("❌ All fields are required and amount must be greater than 0.")

# ================= MONTHLY BUDGET CHECK =================
if st.session_state.expenses:
    last_date = st.session_state.expenses[-1]["Date"]
    month_year = last_date.strftime("%m-%y")

    monthly_total = sum(
        e["Amount"]
        for e in st.session_state.expenses
        if e["Date"].strftime("%m-%y") == month_year
    )

    if monthly_total > monthly_budget and monthly_budget > 0:
        if not st.session_state.budget_alert_shown:
            alert_dialog()
            st.session_state.budget_alert_shown = True
    else:
        st.session_state.budget_alert_shown = False

# ================= VIEW EXPENSES =================
st.header("📋 View Expenses")

if st.session_state.expenses:
    rows = []
    for i, e in enumerate(st.session_state.expenses, start=1):
        rows.append({
            "S.No": i,
            "Date": e["Date"].strftime("%d-%m-%Y"),
            "Amount": e["Amount"],
            "Category": e["Category"],
            "Description": e["Description"]
        })

    df = pd.DataFrame(rows)
    st.dataframe(df, hide_index=True)
else:
    st.info("No Expenses Recorded Yet.")

# ================= DELETE EXPENSE =================
st.header("🗑️ Delete Expense")

# delete success message (ONLY here)
if st.session_state.delete_success:
    st.success("✅ Expense Deleted Successfully!")
    st.session_state.delete_success = False

if st.session_state.expenses:
    expense_str = [
        f"{e['Date'].strftime('%d-%m-%y')} | {e['Category']} | ₹{e['Amount']} | {e['Description']}"
        for e in st.session_state.expenses
    ]

    del_index = st.selectbox(
        "Select Expense to Delete:",
        range(len(expense_str)),
        format_func=lambda x: expense_str[x]
    )

    confirm_del = st.checkbox("Confirm Deletion")

    if st.button("Delete Selected Expense"):
        if confirm_del:
            st.session_state.expenses.pop(del_index)
            st.session_state.delete_success = True
            st.rerun()
        else:
            st.warning("❌ Please confirm deletion.")
else:
    st.info("No Expenses Recorded Yet.")

# ================= UPDATE EXPENSE =================
st.header("✏️ Update Expense")

# update success message (ONLY here)
if st.session_state.update_success:
    st.success("✅ Expense Updated Successfully!")
    st.session_state.update_success = False

if st.session_state.expenses:
    expense_str = [
        f"{e['Date'].strftime('%d-%m-%y')} | {e['Category']} | ₹{e['Amount']} | {e['Description']}"
        for e in st.session_state.expenses
    ]

    update_index = st.selectbox(
        "Select Expense to Update:",
        range(len(expense_str)),
        format_func=lambda x: expense_str[x]
    )

    expense = st.session_state.expenses[update_index]

    with st.form(key=f"update_form_{update_index}"):
        new_date = st.date_input("Date of Expense:", value=expense["Date"])
        new_amount = st.number_input(
            "Amount:", min_value=0.0, step=100.0, value=expense["Amount"]
        )
        new_category = st.text_input("Category:", value=expense["Category"])
        new_description = st.text_area("Description:", value=expense["Description"])

        confirm_update = st.checkbox("Confirm Update Details ✔️")
        submit_update = st.form_submit_button("Update Expense")

        if submit_update:
            if not confirm_update:
                st.error("❌ Please confirm update.")
            elif new_category and new_amount > 0:
                st.session_state.expenses[update_index] = {
                    "Date": new_date,
                    "Amount": new_amount,
                    "Category": new_category,
                    "Description": new_description
                }
                st.session_state.update_success = True
                st.rerun()
            else:
                st.error("❌ All fields are required and amount must be greater than 0.")
else:
    st.info("No Expenses Recorded Yet.")

# ================= TOTAL MONTHLY EXPENSES =================
st.header("💰 Total Expenses")

if st.session_state.expenses:
    months = sorted({e["Date"].strftime("%m-%y") for e in st.session_state.expenses})
    select_month = st.selectbox("Select Month and Year:", months)

    total = sum(
        e["Amount"]
        for e in st.session_state.expenses
        if e["Date"].strftime("%m-%y") == select_month
    )

    st.success(f"Total Expenses for {select_month}: ₹{total}")
else:
    st.info("No Expenses Recorded Yet.")

# ================= CATEGORY-WISE SUMMARY =================
st.header("📊 Category-wise Monthly Summary")

if st.session_state.expenses:
    select_month_summary = st.selectbox(
        "Select Month and Year for Summary:",
        months,
        key="summary_month"
    )

    category_summary = {}
    for e in st.session_state.expenses:
        if e["Date"].strftime("%m-%y") == select_month_summary:
            category_summary[e["Category"]] = (
                category_summary.get(e["Category"], 0) + e["Amount"]
            )

    if category_summary:
        summary_df = pd.DataFrame(
            [{"Category": k, "Total Amount": v} for k, v in category_summary.items()]
        )
        st.table(summary_df)
    else:
        st.info("No expenses for selected month.")
else:
    st.info("No Expenses Recorded Yet.")

# ================= FOOTER =================
st.markdown("👋 Thanks for using the Expense Tracker!")

#python -m streamlit run App\expense_tracker.py - use this command to run the app