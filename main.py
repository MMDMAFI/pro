
import tkinter as tk
from tkinter import messagebox
from user import User
from transaction import Transaction
from database import Database
import report

class FinanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Finance Manager")
        self.users = Database.load_data('users.json')
        self.transactions = Database.load_data('transactions.json')
        self.current_user = None
        self.create_widgets()

    def create_widgets(self):
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(pady=20)

        self.login_frame = tk.Frame(self.main_frame)
        self.register_frame = tk.Frame(self.main_frame)
        self.dashboard_frame = tk.Frame(self.main_frame)

        self.show_login_screen()

    def show_login_screen(self):
        self.clear_frames()
        self.login_frame.pack()

        tk.Label(self.login_frame, text="Username").grid(row=0, column=0)
        self.username_entry = tk.Entry(self.login_frame)
        self.username_entry.grid(row=0, column=1)

        tk.Label(self.login_frame, text="Password").grid(row=1, column=0)
        self.password_entry = tk.Entry(self.login_frame, show="*")
        self.password_entry.grid(row=1, column=1)

        tk.Button(self.login_frame, text="Login", command=self.login).grid(row=2, column=0, columnspan=2)
        tk.Button(self.login_frame, text="Register", command=self.show_register_screen).grid(row=3, column=0, columnspan=2)

    def show_register_screen(self):
        self.clear_frames()
        self.register_frame.pack()

        tk.Label(self.register_frame, text="Username").grid(row=0, column=0)
        self.register_username_entry = tk.Entry(self.register_frame)
        self.register_username_entry.grid(row=0, column=1)

        tk.Label(self.register_frame, text="Password").grid(row=1, column=0)
        self.register_password_entry = tk.Entry(self.register_frame, show="*")
        self.register_password_entry.grid(row=1, column=1)

        tk.Button(self.register_frame, text="Register", command=self.register).grid(row=2, column=0, columnspan=2)
        tk.Button(self.register_frame, text="Back", command=self.show_login_screen).grid(row=3, column=0, columnspan=2)

    def show_dashboard(self):
        self.clear_frames()
        self.dashboard_frame.pack()

        tk.Button(self.dashboard_frame, text="Add Transaction", command=self.show_add_transaction_screen).pack()
        tk.Button(self.dashboard_frame, text="View Transactions", command=self.show_view_transactions_screen).pack()
        tk.Button(self.dashboard_frame, text="Generate Report", command=self.generate_report).pack()
        tk.Button(self.dashboard_frame, text="Logout", command=self.logout).pack()

    def show_add_transaction_screen(self):
        self.clear_frames()
        self.add_transaction_frame = tk.Frame(self.main_frame)
        self.add_transaction_frame.pack()

        tk.Label(self.add_transaction_frame, text="Amount").grid(row=0, column=0)
        self.amount_entry = tk.Entry(self.add_transaction_frame)
        self.amount_entry.grid(row=0, column=1)

        tk.Label(self.add_transaction_frame, text="Date (YYYY-MM-DD)").grid(row=1, column=0)
        self.date_entry = tk.Entry(self.add_transaction_frame)
        self.date_entry.grid(row=1, column=1)

        tk.Label(self.add_transaction_frame, text="Category").grid(row=2, column=0)
        self.category_entry = tk.Entry(self.add_transaction_frame)
        self.category_entry.grid(row=2, column=1)

        tk.Label(self.add_transaction_frame, text="Type (income/expense)").grid(row=3, column=0)
        self.type_entry = tk.Entry(self.add_transaction_frame)
        self.type_entry.grid(row=3, column=1)

        tk.Button(self.add_transaction_frame, text="Add", command=self.add_transaction).grid(row=4, column=0, columnspan=2)
        tk.Button(self.add_transaction_frame, text="Back", command=self.show_dashboard).grid(row=5, column=0, columnspan=2)

    def show_view_transactions_screen(self):
        self.clear_frames()
        self.view_transactions_frame = tk.Frame(self.main_frame)
        self.view_transactions_frame.pack()

        for transaction in self.transactions:
            tk.Label(self.view_transactions_frame, text=str(transaction)).pack()

        tk.Button(self.view_transactions_frame, text="Back", command=self.show_dashboard).pack()

    def clear_frames(self):
        for widget in self.main_frame.winfo_children():
            widget.pack_forget()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if User.validate_user(self.users, username, password):
            self.current_user = username
            self.show_dashboard()
        else:
            messagebox.showerror("Error", "Invalid username or password")

    def register(self):
        username = self.register_username_entry.get()
        password = self.register_password_entry.get()
        self.users.append(User(username, password))
        Database.save_data('users.json', [user.__dict__ for user in self.users])
        messagebox.showinfo("Success", "User registered successfully")
        self.show_login_screen()

    def add_transaction(self):
        amount = float(self.amount_entry.get())
        date = self.date_entry.get()
        category = self.category_entry.get()
        type_ = self.type_entry.get()
        self.transactions.append(Transaction(amount, date, category, type_))
        Database.save_data('transactions.json', [transaction.__dict__ for transaction in self.transactions])
        messagebox.showinfo("Success", "Transaction added successfully")
        self.show_dashboard()

    def generate_report(self):
        rep = report.generate_report(self.transactions)
        report.print_report(rep)
        messagebox.showinfo("Report", "Report generated in console")
        self.show_dashboard()

    def logout(self):
        self.current_user = None
        self.show_login_screen()

if __name__ == "__main__":
    root = tk.Tk()
    app = FinanceApp(root)
    root.mainloop()
