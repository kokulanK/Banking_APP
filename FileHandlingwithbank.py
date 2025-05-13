#   Kokulan Kugathasan
#   UT010840
#   Unicom Tic
#   Mini Banking System 

from datetime import datetime

accounts = {}   #  Dictionary to store the account details 
account_counter = 1000  # Starting account number from 1000

#   Create the account [1. Create Account] ========================================================================

def create_account(): 
    global accounts
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
                save_data()
                account_counter += 1
                break
            else:
                print("Initial balance cannot be negative.")
        except ValueError:
            print("Invalid input. Please enter a number.")

#   ==============================================================================================================

#   Authentication checking process Function =====================================================================

def authenticate():
    global accounts
    while True:
        try:
            account_number = int(input("Enter your account number: "))
            if account_number in accounts:
                print("- Hi", accounts[account_number]['name'], "- Welcome back to our bank service")
                for attempt in range(1, 4):  # 3 attempts total
                    password = input(f'Enter your password (attempt {attempt}/3): ').strip()
                    print(accounts[account_number]['password'])
                    print(password)
                    if accounts[account_number]['password'] == password:
                        return account_number
                    else:
                        print("Incorrect password. Try again.") 
                print("Too many incorrect attempts. Access denied.")
                break
            else:
                print("Re-enter the correct account number.") 
        except ValueError:
            print("Invalid account number.")

#   ==============================================================================================================

#   Deposit Function [2. Deposit Money]===========================================================================

def deposit_money():
    #account_number = authenticate()
    while True:
        try:
            account_number = int(input('Enter the account number you want to deposite : '))
            if account_number in accounts:
                print('The account holder name is : ', accounts[account_number]['name'] )
                print('Name Is Correct Enter: 1 ')
                print('You Dont want to deposite press the number is : 2')
                choice = int(input('Enter (1 or 2): '))
                if choice == 1:
                    amount = float(input("Enter amount to deposit: "))
                    if amount > 0:
                        accounts[account_number]['balance'] += amount
                        accounts[account_number]['transactions'].append("Deposited: " + str(amount))
                        print("Deposited", amount, "successfully!")
                        save_data()
                        break
                    else:
                        print("Amount must be positive or greater than zero.")
                elif choice == 2:
                    print('Thanks for using the banking system!')
                    break
                else:
                    print('Invalid choice. Please enter a number from 1 to 3.')
            else:
                print("Name is incorrect. Please verify the account number or try again.")
        except ValueError:
            print("Invalid Account Number.")

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
    print(account_number)

    print("=============================================")
    print("Transaction History for #", account_number, "[", accounts[account_number]['name'], "]")
    print("=============================================")

    # date_Time = accounts[account_number]['created_date_and_time']
    # print('Account created in : ', date_Time)
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

#   File handling =================================================================================================

#   Load data from a text file ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

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

#   Save data to a text file ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++  

def save_data():
    with open("bank_data.txt", "w") as f:
        f.write("AccountCounter: " + str(account_counter) + "\n\n")
        for acc_num, details in accounts.items():
            f.write('Account Number: ' + str(acc_num) + "\n")
            f.write('Created time is ' + str(datetime.now()) + "\n")
            f.write("Name: " + details['name'] + "\n")
            f.write("Password: " + details['password'] + "\n")
            f.write("PIN: " + str(details['pin']) + "\n")
            f.write("Balance: " + str(details['balance']) + "\n")
            f.write("Password Changes: " + str(details['times_of_password_changed']) + "\n")
            f.write("Transactions:\n")
            for txn in details['transactions']:
                f.write("  - " + txn + "\n")
            f.write("\n")


#   ===============================================================================================================

#   Main Manager class ============================================================================================    

def main_Manager_menu():
    set_password = '123456'
    while True:
        try:
            print('=====================================================')
            print('        Welcome To Mini Banking Manager Section      ')
            print('=====================================================')
            new_password = input('Enter the Pin : ').strip()
            if set_password == new_password:
                print('1. Create Account')
                print('2. Calculate Interest')
                print('3. Exit')
                choice = int(input("Enter your choice (1-3): "))
                if choice == 1:
                    create_account()
                elif choice == 2:
                    calculate_interest()
                elif choice == 3:
                    print("Thanks for using the banking system!") 
                    break
                else:
                    print("Invalid choice. Please enter a number from 1 to 3.")
            else:
                print("Re-enter the correct Password.") 
        except ValueError:
            print('Invalid input! Please enter a number between 1 and 3.')
#   ===============================================================================================================    

#   Main Customer class  ==========================================================================================

def main_Coustomer_menu():
    while True:
        print('======================================================')
        print('        Welcome To Mini Banking Customer Section      ')
        print('======================================================')
        print('1. Deposit Money')
        print('2. Withdraw Money')
        print('3. Check Balance')
        print('4. Transaction History')
        print('5. Forget the password')
        print('6. Exit')
        
        choice = int(input("Enter your choice (1-9): "))

        try:
            if choice == 1:
                deposit_money()
            elif choice == 2:
                withdraw_money()
            elif choice == 3:
                check_balance()
            elif choice == 4:
                transaction_history()
            elif choice == 5:
                forget_password()
            elif choice == 6:
                print("Thanks for using the banking system!") 
                break
            else:
                print("Invalid choice. Please enter a number from 1 to 9.")
        except ValueError:
            print('Invalid input! Please enter a number between 1 and 3.')


#   ===============================================================================================================

#   Login Page ====================================================================================================

def start_Function():
    while True:
        print('=============================================')
        print('        Welcome To Mini Banking System       ')
        print('=============================================')
        print('Please select your role:')
        print(' [1] Customer')
        print(' [2] Manager')
        print(' [3] Exit')

        try:
            choice = int(input())
            if choice == 1:
                main_Coustomer_menu()
            elif choice == 2:
                main_Manager_menu()
            elif choice == 3:
                print('Thanks for using the banking system!') 
                break  
            else:
                print('Invalid choice. Please enter a number from 1 to 3.')
        except ValueError:
            print('Invalid input! Please enter a number between 1 and 3.')

#   ===============================================================================================================


#   Start the function With load the data  ========================================================================

load_data()
start_Function() 

#   ===============================================================================================================

#   Updated code on 6.16pm__13/05/2025

#   ===============================================================================================================
