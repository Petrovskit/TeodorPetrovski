def print_my_name():
    name = "Teodor Petrovski"
    print(name)


print("Printing my name.")
print_my_name()


def print_numbers():
    for i in range(0, 11):
        print(i)


print("------------------------------")
print("Printing first 10 numbers.")
print_numbers()


def print_odd_numbers():
    for i in range(1, 20, 2):
        print(i)


print("------------------------------")
print("Printing first 10 odd numbers.")
print_odd_numbers()


def multiply_entered_number_by_two():
    user_input = input("Please enter a number: ")

    if user_input.isdigit():
        num = int(user_input)
        result = num * 2
        print("------------------------------")
        print("Your entered number multiplied by 2 is:", result)
    else:
        print("Only numbers are allowed!")


multiply_entered_number_by_two()


def characters_in_name():
    user_input = input("Please enter your name: ")

    if user_input.isalpha():
        char_count = len(user_input)
        print(f"Your '{user_input}' has {char_count} characters.")
    else:
        print("I am pretty sure that your name does not have numbers or special characters in it :)")


characters_in_name()
