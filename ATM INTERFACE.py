import random

class ComprehensiveATM:
    def main(self):
        bank = Bank()

        while True:
            print("Welcome to the Comprehensive ATM System!")
            print("1. Login")
            print("2. Create an Account")
            print("3. Exit")
            choice = int(input("Please select an option: "))

            if choice == 1:
                bank.login()
            elif choice == 2:
                bank.create_account()
            elif choice == 3:
                print("Thank you for using the Comprehensive ATM System.")
                return
            else:
                print("Invalid choice. Please try again.")

class Bank:
    accounts = {}
    random = random.Random()

    def login(self):
        account_number = int(input("Enter your account number: "))

        account = self.accounts.get(account_number)
        if account and not account.is_locked():
            password = input("Enter your password: ")
            if account.authenticate(password):
                print("Login successful!")
                account.unlock()
                account.show_options()
            else:
                print("Invalid password.")
                account.increment_login_attempts()
                if account.get_login_attempts() >= 3:
                    print("Your account has been locked. Please contact customer support.")
                    account.lock()
        else:
            print("Invalid account number or account locked.")

    def create_account(self):
        name = input("Enter your name: ")
        password = input("Enter a password: ")
        balance = float(input("Enter initial balance: "))
        currency = input("Enter currency (USD, EUR, INR): ").upper()

        if currency not in ("USD", "EUR", "INR"):
            print("Invalid currency. Only USD, EUR, and INR are supported.")
            return

        account_number = self.generate_account_number()
        account = Account(account_number, name, password, balance, currency)
        self.accounts[account.get_account_number()] = account
        print("Account created successfully. Your account number is:", account.get_account_number())

    def generate_account_number(self):
        return 100000 + self.random.randint(0, 900000)

class Account:
    def __init__(self, account_number, name, password, balance, currency):
        self.account_number = account_number
        self.name = name
        self.password = password
        self.balance = balance
        self.currency = currency
        self.transaction_history = []
        self.locked = False
        self.login_attempts = 0

    def get_account_number(self):
        return self.account_number

    def authenticate(self, entered_password):
        return self.password == entered_password

    def show_options(self):
        while True:
            print("\nAccount Options:")
            print("1. Check Balance")
            print("2. Deposit")
            print("3. Withdraw")
            print("4. Change Password")
            print("5. Transfer Money")
            print("6. View Transaction History")
            print("7. Logout")
            choice = int(input("Please select an option: "))
            if choice == 1:
                self.check_balance()
            elif choice == 2:
                self.deposit()
            elif choice == 3:
                self.withdraw()
            elif choice == 4:
                self.change_password()
            elif choice == 5:
                self.transfer()
            elif choice == 6:
                self.view_transaction_history()
            elif choice == 7:
                print("Logged out successfully.")
                return
            else:
                print("Invalid choice. Please try again.")

    def check_balance(self):
        print("Current balance:", self.format_currency(self.balance))

    def deposit(self):
        amount = float(input("Enter deposit amount: "))
        if amount <= 0:
            print("Invalid amount. Deposit amount must be greater than zero.")
            return
        self.balance += amount
        self.transaction_history.append("Deposited " + self.format_currency(amount))
        print("Deposit successful. Current balance:", self.format_currency(self.balance))

    def withdraw(self):
        amount = float(input("Enter withdrawal amount: "))
        if amount <= 0:
            print("Invalid amount. Withdrawal amount must be greater than zero.")
            return
        if amount > self.balance:
            print("Insufficient funds.")
        else:
            self.balance -= amount
            self.transaction_history.append("Withdrawn " + self.format_currency(amount))
            print("Withdrawal successful. Current balance:", self.format_currency(self.balance))

    def change_password(self):
        current_password = input("Enter current password: ")
        if not self.authenticate(current_password):
            print("Incorrect password.")
            return
        new_password = input("Enter new password: ")
        self.password = new_password
        print("Password changed successfully.")

    def transfer(self):
        recipient_account_number = int(input("Enter recipient's account number: "))
        recipient = Bank.accounts.get(recipient_account_number)
        if not recipient:
            print("Recipient account not found.")
            return
        amount = float(input("Enter transfer amount: "))
        if amount <= 0:
            print("Invalid amount. Transfer amount must be greater than zero.")
            return
        if amount > self.balance:
            print("Insufficient funds.")
        else:
            self.balance -= amount
            recipient.balance += amount
            self.transaction_history.append("Transferred " + self.format_currency(amount) + " to account " + str(recipient_account_number))
            print("Transfer successful. Current balance:", self.format_currency(self.balance))

    def view_transaction_history(self):
        print("Transaction history for account number:", self.account_number)
        for transaction in self.transaction_history:
            print(transaction)

    def is_locked(self):
        return self.locked

    def lock(self):
        self.locked = True

    def unlock(self):
        self.locked = False
        self.login_attempts = 0

    def get_login_attempts(self):
        return self.login_attempts

    def increment_login_attempts(self):
        self.login_attempts += 1

    def format_currency(self, amount):
        return self.currency + " " + "{:.2f}".format(amount)

if __name__ == "__main__":
    atm = ComprehensiveATM()
    atm.main()
