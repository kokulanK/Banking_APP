#   Kokulan Kugathasan
#   UT010840
#   Unicom Tic
#   Mini Banking System 

accounts = {}   #  Dictionary to store the account details 
account_counter = 1000  # Starting account number from 1000

#   Create the account [1. Create Account] ========================================================================

def create_account(): 
    global account_counter
    name = input("Enter account holder name: ").strip()
    password = input("Set a password for your account: ").strip()
    security_pin = int(input("Set a 4-digit security PIN (for password recovery): ").strip())
    while True:
        try:
            initial_balance = float(input("Enter initial balance: "))
            if initial_balance > 0:
                accounts[account_counter] = {
                    'name': name,
                    'password': password,
                    'pin': security_pin,
                    'balance': initial_balance,
                    'times_of_password_changed': 0,
                    'transactions': ["Account created with initial balance: " + str(initial_balance)]
                }
                print("Account created successfully! Your account number is", account_counter)
                account_counter += 1
                save_data()
                break
            else:
                print("Initial balance cannot be negative.")
        except ValueError:
            print("Invalid input. Please enter a number.")

#   ==============================================================================================================

#   Authentication checking process Function =====================================================================

def authenticate():
    while True:
        try:
            account_number = int(input("Enter your account number: "))
            if account_number in accounts:
                print("- Hi", accounts[account_number]['name'], "- Welcome back to our bank service")
                for attempt in range(1, 4):  # 3 attempts total
                    password = input(f'Enter your password (attempt {attempt}/3): ').strip()
                    if accounts[account_number]['password'] == password:
                        return account_number
                    else:
                        print("Incorrect password. Try again.") 
                print("Too many incorrect attempts. Access denied.")
                return False
            else:
                print("Re-enter the correct account number.") 
        except ValueError:
            print("Invalid account number.")

#   ==============================================================================================================

#   Deposit Function [2. Deposit Money]===========================================================================

def deposit_money():
    account_number = authenticate()
    while True:
        try:
            amount = float(input("Enter amount to deposit: "))
            if amount > 0:
                accounts[account_number]['balance'] += amount
                accounts[account_number]['transactions'].append("Deposited: " + str(amount))
                print("Deposited", amount, "successfully!")
                print("Your final balance is:", accounts[account_number]['balance'])
                save_data()
                break
            else:
                print("Amount must be positive or greater than zero.")
        except ValueError:
            print("Invalid amount.")

#   ===============================================================================================================

#   Withdraw Money Function [3. Withdraw Money]====================================================================

def withdraw_money():
    account_number = authenticate()
    while True:
        try:
            if account_number == False:
                break
            amount = float(input('Enter amount to withdraw: '))
            if amount > 0:
                if amount <= accounts[account_number]['balance']:
                    accounts[account_number]['balance'] -= amount
                    accounts[account_number]['transactions'].append("Withdrew: " + str(amount))
                    print('Withdrew', amount, 'successfully!')
                    print("Your final balance is:", accounts[account_number]['balance'])
                    save_data()
                    break
                else:
                    print('Balance is not enough')
                    print('Your eligible balance is', accounts[account_number]['balance'])
            else:
                print("Amount must be positive or greater than zero.")
        except ValueError:
            print("Invalid amount.")

#   ===============================================================================================================

#   Balance Checking [4. Check Balance]============================================================================

def check_balance():
    while True:
        account_number = authenticate()
        if account_number == True:
            print("Your final balance is:", accounts[account_number]['balance'])
        break

#   ===============================================================================================================

#   Transaction History [5. Transaction History]===================================================================

def transaction_history():
    account_number = authenticate()
    while True:
        if account_number == True:
            print("========================================")
            print("Transaction History for #", account_number, "[", accounts[account_number]['name'], "]")
            print("========================================")

            transactions = accounts[account_number]['transactions']

            if len(transactions) == 0:
                print("No transactions found.")
            else:
                count = 1
                for txn in transactions:
                    print(str(count) + ". " + str(txn))
                    count += 1
            save_data()

            print("========================================\n")
            break

#   ===============================================================================================================

#   Transfer Money [6. Transfer Money]=============================================================================

def transfer_money():
    from_acc = input("Enter your account number: ").strip()
    if not from_acc.isdigit() or int(from_acc) not in accounts:
        print("Account does not exist.")
        return
    from_acc = int(from_acc)

    if from_acc != authenticate():
        return

    to_acc = input("Enter recipient account number: ").strip()
    if not to_acc.isdigit() or int(to_acc) not in accounts:
        print("Recipient account does not exist.")
        return
    to_acc = int(to_acc)

    try:
        amount = float(input("Enter amount to transfer: "))
        if amount <= 0:
            print("Amount must be positive.")
            return
        if amount > accounts[from_acc]['balance']:
            print("Insufficient funds.")
            return
        accounts[from_acc]['balance'] -= amount
        accounts[to_acc]['balance'] += amount
        accounts[from_acc]['transactions'].append("Transferred " + str(amount) + " to " + str(to_acc))
        accounts[to_acc]['transactions'].append("Received " + str(amount) + " from " + str(from_acc))
        print("Transferred", amount, "successfully!")
        save_data()
    except ValueError:
        print("Invalid amount.")

#   ===============================================================================================================

#   Calculate the interest [7. Calculate Interest]=================================================================

def calculate_interest():
    rate = 0.05  # 5% interest
    for acc in accounts:
        interest = accounts[acc]['balance'] * rate
        accounts[acc]['balance'] += interest
        accounts[acc]['transactions'].append("Interest added: " + str(interest))
    print("Interest added to all accounts.")
    save_data()
   
#   ===============================================================================================================

#   Forget the Password [8. Forget the password]===================================================================

def forget_password():
    while True:
        try:
            account_number = int(input('Enter your account number: '))
            if account_number == False:
                break
            if account_number in accounts:
                print("- Hi", accounts[account_number]['name'], '- Let\'s recover your password')
                for attempt in range(1, 4):  
                    pin_input = input(f'Enter your 4-digit security PIN (attempt {attempt}/3): ').strip()
                    if pin_input == str(accounts[account_number]['pin']):
                        new_password = input('Enter your new password: ').strip()
                        confirm_password = input('Confirm your new password: ').strip()
                        if new_password == confirm_password:
                            accounts[account_number]['password'] = new_password
                            print('Password has been reset successfully.')
                            accounts[account_number]['times_of_password_changed'] += 1
                            accounts[account_number]['transactions'].append("Password changed count: " + str(accounts[account_number]['times_of_password_changed']))
                            save_data()
                            break
                        else:
                            print('Passwords do not match. Try again.')
                    elif attempt < 3:
                        print('Incorrect PIN. Try again.')
                print('Too many incorrect attempts. Access denied.')
            else:
                print('Re-enter the correct account number.')
        except ValueError:
            print('Invalid account number.')

#   ===============================================================================================================    

def manager_Class():
    print('Wellcome to the manager Function')
    set_password = 123456
    while True:
        try:
            new_password = int(input('Enter the Pin : '))
            if set_password == new_password:
                print('Hi manager welcome to the manager login')
                for attempt_manager in range(1, 4):  # 3 attempts total
                    new_password = input(f'Enter your password (attempt {attempt_manager}/3): ').strip()
                    if set_password == new_password:
#   Start edit in here ==========================================
                        print("1. Create Account")
                        print("7. Calculate Interest")
                        choice = input("Enter your choice (1-9): ").strip()

                        if choice == '1':
                            create_account()
                        elif choice == '7':
                            calculate_interest()

                        return 1     #  Strat coding in here onawards
                    else:
                        print("Incorrect password. Try again.") 
                print("Too many incorrect attempts. Access denied.")
                return -1
            else:
                print("Re-enter the correct account number.") 
        except ValueError:
            print("Invalid account number.")

#   Main Function =================================================================================================

def main_menu():
    while True:
        print("\n=== Mini Banking System For our valuable coustermer ===")
        
        print("2. Deposit Money")
        print("3. Withdraw Money")
        print("4. Check Balance")
        print("5. Transaction History")
        print("6. Transfer Money")
        print("7. Calculate Interest")
        print("8. Forget the password")
        
        print("10. Exit")
        choice = input("Enter your choice (1-9): ").strip()

        if choice == '1':
            create_account()
        elif choice == '2':
            deposit_money()
        elif choice == '3':
            withdraw_money()
        elif choice == '4':
            check_balance()
        elif choice == '5':
            transaction_history()
        elif choice == '6':
            transfer_money()
        
        elif choice == '8':
            forget_password()
        elif choice == '10':
            print("Thanks for using the banking system!") 
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 9.")

#   ===============================================================================================================

#   File handling =================================================================================================

# Save data to a text file

def save_data():
    with open("bank_data.txt", "w") as f:
        f.write("AccountCounter: " + str(account_counter) + "\n\n")
        for acc_num, details in accounts.items():
            f.write('Account Number: ' , str(acc_num))
            f.write("Name: " + details['name'] + "\n")
            f.write("Password: " + details['password'] + "\n")
            f.write("PIN: " + str(details['pin']) + "\n")
            f.write("Balance: " + str(details['balance']) + "\n")
            f.write("Password Changes: " + str(details['times_of_password_changed']) + "\n")
            f.write("Transactions:\n")
            for txn in details['transactions']:
                f.write("  - " + txn + "\n")
            f.write("\n")  # blank line between accounts


# Load data from a text file

def load_data():
    global account_counter
    try:
        with open("bank_data.txt", "r") as f:
            lines = f.readlines()

        current_account = {}
        acc_num = None
        transactions = []
        for line in lines:
            line = line.strip()
            if not line:
                if acc_num and current_account:
                    current_account['transactions'] = transactions
                    accounts[acc_num] = current_account
                # Reset for next account
                current_account = {}
                transactions = []
                acc_num = None
                continue

            if line.startswith("AccountCounter:"):
                account_counter = int(line.split(":")[1].strip())
            elif line.startswith("Account Number:"):
                acc_num = int(line.split(":")[1].strip())
            elif line.startswith("Name:"):
                current_account['name'] = line.split(":", 1)[1].strip()
            elif line.startswith("Password:"):
                current_account['password'] = line.split(":", 1)[1].strip()
            elif line.startswith("PIN:"):
                current_account['pin'] = int(line.split(":")[1].strip())
            elif line.startswith("Balance:"):
                current_account['balance'] = float(line.split(":")[1].strip())
            elif line.startswith("Password Changes:"):
                current_account['times_of_password_changed'] = int(line.split(":")[1].strip())
            elif line.startswith("- "):  # transaction line
                transactions.append(line[2:].strip())
            elif line.startswith("Transactions:"):
                continue  # just a label line

        # Catch any remaining account not followed by blank line
        if acc_num and current_account:
            current_account['transactions'] = transactions
            accounts[acc_num] = current_account

    except FileNotFoundError:
        with open("bank_data.txt", "w") as f:
            f.write("AccountCounter: 1000\n\n")


#   ===============================================================================================================



#   Login Page ====================================================================================================

def start_Function():
    while True:
        print('========================================================')
        print('Welcome to the BOC Banking system\n')
        print('If you are the Customer press 1:')
        print('If you are the Admin press 2:')
        num_1 = int(input('You want to exit from this loop press 3: '))  

        if num_1 == 1:
            main_menu()
        elif num_1 == 2:
            manager_Class()
        elif num_1 == 3:
            print("Thanks for using the banking system!") 
            break  # This exits the while loop (i.e., the function stops here)
        else:
            print("Invalid choice. Please enter a number from 1 to 3.")

#   ===============================================================================================================

#   Start the function With load the data  ========================================================================

load_data()
start_Function() 



#   ===============================================================================================================

