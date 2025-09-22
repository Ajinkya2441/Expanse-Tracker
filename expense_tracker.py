import json
import os
from datetime import datetime

EXPENSE_FILE = "expenses.json"

def load_expenses():
    if not os.path.exists(EXPENSE_FILE):
        return []
    try:
        with open(EXPENSE_FILE, "r") as f:
            data = json.load(f)
            if not isinstance(data, list):
                print("⚠️ Warning: Expense file corrupted, resetting data.")
                return []
            return data
    except json.JSONDecodeError:
        print("⚠️ Error: Could not parse JSON. Starting with empty expenses.")
        return []

def save_expenses(expenses):
    with open(EXPENSE_FILE, "w") as f:
        json.dump(expenses, f, indent=4)

def parse_date(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        return None

def add_expense():
    print("\nAdd New Expense")
    date_str = input("Date (YYYY-MM-DD) [leave empty for today]: ").strip()
    if date_str == "":
        date = datetime.today()
    else:
        date = parse_date(date_str)
        if not date:
            print("❌ Invalid date format. Use YYYY-MM-DD.")
            return

    category = input("Category (e.g. Food, Transport): ").strip()
    if not category:
        print("❌ Category is required.")
        return

    amount_str = input("Amount: ").strip()
    try:
        amount = float(amount_str)
        if amount <= 0:
            print("❌ Amount must be a positive number.")
            return
    except ValueError:
        print("❌ Invalid amount entered.")
        return

    notes = input("Notes (optional): ").strip()

    expenses = load_expenses()
    expenses.append({
        "date": date.strftime("%Y-%m-%d"),
        "category": category,
        "amount": amount,
        "notes": notes
    })
    save_expenses(expenses)
    print("✅ Expense added successfully.")

def view_expenses():
    expenses = load_expenses()
    if not expenses:
        print("\n📭 No expenses recorded yet.")
        return

    print("\n🧾 All Expenses:")
    print(f"{'No.':<5}{'Date':<12}{'Category':<15}{'Amount':<10}{'Notes'}")
    print("-" * 50)
    for i, exp in enumerate(expenses, 1):
        notes_display = exp['notes'] if exp['notes'] else "-"
        print(f"{i:<5}{exp['date']:<12}{exp['category']:<15}${exp['amount']:<9.2f}{notes_display}")

def generate_report():
    expenses = load_expenses()
    if not expenses:
        print("\n📭 No expenses to report.")
        return

    total = sum(e['amount'] for e in expenses)
    print(f"\n📊 Total Expenses: ${total:.2f}")

    summary = {}
    for e in expenses:
        summary[e['category']] = summary.get(e['category'], 0) + e['amount']

    print("\n📋 Expenses by Category:")
    for category, amount in summary.items():
        print(f"- {category}: ${amount:.2f}")

def delete_expense():
    expenses = load_expenses()
    if not expenses:
        print("\n📭 No expenses to delete.")
        return

    view_expenses()
    try:
        idx = int(input("\nEnter expense number to delete: ")) - 1
        if 0 <= idx < len(expenses):
            removed = expenses.pop(idx)
            save_expenses(expenses)
            print(f"🗑️ Removed expense: {removed['category']} on {removed['date']} (${removed['amount']:.2f})")
        else:
            print("❌ Invalid expense number.")
    except ValueError:
        print("❌ Please enter a valid number.")

def show_menu():
    print("""
💰 EXPENSE TRACKER MENU
1. View all expenses
2. Add new expense
3. Generate report
4. Delete an expense
0. Exit
""")

def main():
    while True:
        show_menu()
        choice = input("Enter choice (0-4): ").strip()
        if choice == "1":
            view_expenses()
        elif choice == "2":
            add_expense()
        elif choice == "3":
            generate_report()
        elif choice == "4":
            delete_expense()
        elif choice == "0":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
