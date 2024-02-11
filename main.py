import re
import os  
import sys
from enum import Enum
from colorama import Fore, Style
import json

class ErrorType(Enum):
    INFO = "INFO"
    ERROR = "ERROR"
    DEBUG = "DEBUG"
    WARNING = "WARNING"

error_type_values = [error_type.value for error_type in ErrorType]
log_pattern  = r'\b(?:' + '|'.join(map(re.escape, error_type_values)) + r')\b'
table_text_left = "Рівень логування"
table_text_right = "Кількість повідомлень"
pattern =r'\b\s*\d+\.*\d+\s*\b'

current_directory = os.getcwd()
contacts_file = "contacts.txt"

def log_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return print(Fore.RED + str(e) + Style.RESET_ALL)

    return inner

def get_file_path(file_name: str)->str:
    return os.path.join(current_directory, file_name)

def get_path():
    argv  = sys.argv
    if len(argv) < 2:
        return ""
    return argv[1]

file_path = get_path()

def caching_fibonacci ():
    cache = {}
    def fibonacci(n: int):
        if n in cache:
            return cache[n]
        if n <= 1:
            result = n
        else:
            result = fibonacci(n-1) + fibonacci(n-2)
        cache[n] = result
        return result

    return fibonacci

def generator_numbers(numbersStr: list[str]):
    for number in numbersStr:
        yield float(number)
   
@log_error
def sum_profit(text: str, func: callable = generator_numbers ):
    if not isinstance(text, str):
        raise Exception("The input text must be a string")
    
    numbers = re.findall(pattern, text)
    if not numbers:
        return 0
    
    result = 0
    for number in func(numbers):
        result += number
    return result

@log_error
def load_logs():
    if not file_path:
        raise Exception("File path is empty")
    
    try:
        with open(file_path, 'r') as file:
            return file.read()
    
    except Exception as e:
        return e

@log_error  
def parse_log_line(log_line: str):
    try:
        return re.findall(log_pattern, log_line)
    except Exception as e:
        return str(e)    

@log_error
def count_log():
    try:
        logText = load_logs()
        if not logText:
            raise Exception("Log is empty")
        logs = parse_log_line(logText)
        return {log: logs.count(log) for log in error_type_values}
    except Exception as e:
        return str(e)
    
def print_logs():
    logs: dict = count_log()
    print (table_text_left + " | " + table_text_right )
    row_ui_left = "-"*len(table_text_left)
    row_ui_right = "-"*len(table_text_right)
    for key, value in logs.items():
        print(row_ui_left + " | " + row_ui_right)
        print(key + " " *  +( len(table_text_left) - len(key) ) + " |   " + str(value))    
        print(row_ui_left + " | " + row_ui_right)

@log_error
def add_user(user: list):
    if not user or len(user) < 2:
      raise  Exception("Name and phone are required")
    name = user[0]
    phone = user[1]
    users = get_users()
    try:
        with open(get_file_path(contacts_file), "w") as file:
            contacts_lsit = [
                {"name": name, "phone": phone},
            ]

            if(len(users)):
                contacts_lsit.extend(users)
            data =json.dumps(contacts_lsit)
            print("users",data)

            file.write(data)
            print(Fore.CYAN + "User added successfully" + Style.RESET_ALL)   
    except FileNotFoundError as e:
        raise Exception("Something went wrong!")

@log_error
def change_user_contact(name:str):
    if not name :
        parse_input()
        raise Exception("Name is required")
    
    contacts:list[dict] =  get_users()    
    try:
        with open(get_file_path(contacts_file), "w") as file:
            for i in range(len(contacts)):
                if name.lower() in contacts[i].get("name").lower():
                    phone = input("Enter new phone number: ")
                    contacts[i]["phone"] = phone
                    file.write(json.dumps(contacts))
                    print(Fore.GREEN + "User contact changed successfully" + Style.RESET_ALL) 
                    return
            print(Fore.RED +"User not found")
    except FileNotFoundError as e:
        raise Exception(e)

@log_error
def get_user_contact(name:str):
    if not name:
        parse_input()
        raise Exception("Name is required")
    try:
        with open(get_file_path(contacts_file), "r") as file:
            contacts:dict = json.loads(file.read())
            for contact in contacts:
                if name in contact:
                    print(contact.name, contact.phone)
                    return
            print(Fore.RED +"User not found" + + Style.RESET_ALL)
    except FileNotFoundError as e:
        print("Something went wrong!",Fore.RED + e)        

@log_error
def print_all_users():
    try:
        users = get_users()
        if not len(users):
            raise Exception("No users found")
        for user in users:
             print(user.get("name"), user.get("phone"))
    except FileNotFoundError as e:
        raise Exception(e)
    
@log_error
def get_users()->list:
    try:
        with open(get_file_path(contacts_file), "r") as file:
            users = file.read()
            if not users:
                return []
            return json.loads(users)
    except FileNotFoundError as e:
        raise Exception(e)

@log_error
def parse_input():
    comand = {
        "1": "Add",
        "2": "Change",
        "3": "All",
        "4": "Exit"
    }
    for key, value in comand.items():
        print(Fore.GREEN + f"{key}: {value}" + Style.RESET_ALL)
    
    choice = input(Fore.BLUE  + "How can I help you? Choose a command: " + Style.DIM)
    
    if not choice :
        print("Choose a command")
        return   

    choice = choice.lower()
    match choice:
        case "1" | "add":
            user = input("Enter user name and phone number: "  + Style.RESET_ALL).strip().split(" ")
            add_user(user)
        case "2" |"change":
            user = input("Enter user name : "  + Style.RESET_ALL).strip()
            change_user_contact(user)
        case "3" | "all":
            print_all_users()
        case "4" | "exit" | "close" | "quit":
            print("Goodbye!")
            exit()
        case _:
            print("Invalid choice")
            parse_input()
    parse_input()   
    

def main():
    print(Fore.GREEN + "Welcome to Halper Bot!"  + Style.RESET_ALL)
    parse_input()

if __name__ == "__main__":
    main()


print_logs()
# sum_profit("Загальний дохід працівника складається з декількох частин: 1000.01 як основний дохід, доповнений додатковими надходженнями 27.45 і 324.00 доларів.")
# fib = caching_fibonacci()


