from datetime import datetime

class ATM:
    def __init__(self, location, branch_name):
        self.location = location
        self.branch_name = branch_name

    def show(self):
        return f"ATM Location: {self.location}, Branch: {self.branch_name}"


class Account:
    def __init__(self, account_number, owner_name, pin, balance):
        self.account_number = account_number
        self.owner_name = owner_name
        self.pin = pin
        self.balance = balance

    def validate_pin(self, entered_pin):
        return self.pin == entered_pin

    def get_balance(self):
        return self.balance

    def debit(self, amount):
        if amount > self.balance:
            raise ValueError("Insufficient funds")
        self.balance -= amount
        return self.balance

    def credit(self, amount):
        self.balance += amount
        return self.balance


class Transaction:
    def __init__(self, transaction_id, amount, transaction_type):
        self.transaction_id = transaction_id
        self.amount = amount
        self.transaction_type = transaction_type
        self.timestamp = datetime.now()

    def __str__(self):
        return f"{self.timestamp} - {self.transaction_type}: ${self.amount}"


class CashWithdrawal:
    def __init__(self, atm, account):
        self.atm = atm
        self.account = account
        self.transactions = []

    def validate_withdrawal(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        if amount > self.account.get_balance():
            raise ValueError("Insufficient balance")

    def withdraw_cash(self, amount):
        self.validate_withdrawal(amount)
        self.account.debit(amount)
        transaction = Transaction(
            transaction_id=len(self.transactions) + 1,
            amount=amount,
            transaction_type="Withdrawal"
        )
        self.transactions.append(transaction)
        return f"Withdrawn ${amount}. Remaining balance: ${self.account.get_balance()}"

    def log_transaction(self):
        return [str(transaction) for transaction in self.transactions]

    def get_balance(self):
        return self.account.get_balance()


class UserSession:
    def __init__(self):
        self.current_account = None
        self.transactions = []

    def start_session(self, account):
        self.current_account = account
        self.transactions = []

    def end_session(self):
        self.current_account = None
        self.transactions = []

    def add_transaction(self, transaction):
        self.transactions.append(transaction)

    def get_transaction_history(self):
        return [str(transaction) for transaction in self.transactions]

    def is_active(self):
        return self.current_account is not None


# Example Usage
if __name__ == "__main__":
    # Setup ATM and Accounts
    atm = ATM(location="Main Street", branch_name="InfoSuper Bank HQ")
    account = Account(account_number="9876543210", owner_name="Mert Balkaç", pin="5678", balance=1000)

    # Create a User Session
    session = UserSession()
    session.start_session(account)

    # Display ATM Info
    print(atm.show())

    # Handle PIN Validation
    entered_pin = "5678"  # Example user input
    if account.validate_pin(entered_pin):
        print(f"Welcome, {account.owner_name}!")
    else:
        print("Invalid PIN.")

    # Perform a Cash Withdrawal
    withdrawal = CashWithdrawal(atm=atm, account=account)
    try:
        print(withdrawal.withdraw_cash(500))
    except ValueError as e:
        print(e)

    # View Account Balance
    print(f"Current Balance: ${withdrawal.get_balance()}")

    # Log Transactions
    print("Transaction History:")
    print("\n".join(withdrawal.log_transaction()))

    # End User Session
    session.end_session()
    print("Session ended. Thank you for using InfoSuper Bank!")
