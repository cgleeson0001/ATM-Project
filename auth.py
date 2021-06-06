import random
import validation
import database
from getpass import getpass


def init():
    print("Welcome to the Bank")

    have_account = int(input("Do you have an account with us?: 1 (yes) 2 (no) \n"))

    if have_account == 1:

        login()

    elif have_account == 2:

        register()

    else:
        print("You have selected an invalid option")
        init()


def login():
    print("Login to Your Account")
    global account_number_from_user

    account_number_from_user = input("What is Your Account Number? \n")

    is_valid_account_number = validation.account_number_validation(account_number_from_user)

    if is_valid_account_number:

        password = getpass("What is Your Password? \n")

        user = database.authenticated_user(account_number_from_user, password)
        print(user)
        if user:
            bank_operation(user)

        print("Invalid Account Number or Password")
        login()

    else:
        print("Account Number Invalid: Please enter up to 10 digits and only integers")
        init()


def register():
    print("*** Register for an Account Here ***")

    email = input("What is your email address? \n")
    first_name = input("What is your first name? \n")
    last_name = input("What is your last name? \n")
    password = getpass("Create a Password \n")

    account_number = generation_account_number()

    is_user_created = database.create(account_number, first_name, last_name, email, password)

    if is_user_created:

        print("Your Account Has Been Created")
        print(" == ==== ====== ===== ===")
        print("Your account number is: %d" % account_number)
        print("Make sure to keep it safe!")
        print(" == ==== ====== ===== ===")

        login()

    else:
        print("Something went wrong, please try again.")
        register()


def bank_operation(user):
    print("Welcome %s %s" % (user[0], user[1]))

    selected_option = int(input("What would you like to do? (1) Deposit (2) Withdraw Cash (3) Logout (4) Exit \n"))

    if selected_option == 1:

        deposit_operation(user)

    elif selected_option == 2:

        withdrawal_operation(user)

    elif selected_option == 3:

        logout()

    elif selected_option == 4:

        exit()

    else:
        print("Invalid option selected")
        bank_operation(user)


def withdrawal_operation(user):
    current_balance = user[4]
    withdrawal_amount = int(input("Enter the amount you would like to withdraw. \n"))
    current_balance = int(current_balance) - withdrawal_amount
    user[4] = current_balance

    updated_user = user[0] + "," + user[1] + "," + user[2] + "," + user[3] + "," + str(user[4])

    user_db_path = "data/user_record/"
    f = open(user_db_path + str(account_number_from_user) + ".txt", "w")
    f.write(updated_user)
    f.close()

    print("You successfully withdrew {}".format(withdrawal_amount))
    print("Your current balance is now {}".format(current_balance))

    return bank_operation(user)


def deposit_operation(user):
    current_balance = user[4]
    deposit_amount = int(input("Enter the amount you would like to deposit. \n"))
    current_balance = int(current_balance) + deposit_amount
    user[4] = current_balance

    updated_user = user[0] + "," + user[1] + "," + user[2] + "," + user[3] + "," + str(user[4])

    user_db_path = "data/user_record/"
    f = open(user_db_path + str(account_number_from_user) + ".txt", "w")
    f.write(updated_user)
    f.close()

    print("You have successfully deposited {}".format(deposit_amount))
    print("Your current balance is now {}".format(current_balance))

    return bank_operation(user)


def generation_account_number():
    return random.randrange(1111111111, 9999999999)


def set_current_balance(user_details, balance):
    user_details[4] = balance


def get_current_balance(user_details):
    return user_details[4]


def logout():
    login()


init()