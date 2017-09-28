#!/usr/bin/env python3

"""
Safely Retrieves an number from a user firendly input
"""
def ask_for_int(prompt, retries=100, reminder='Please try again!'):
    while True:
        try:
            return int(input(prompt))
        except:
            pass
        
        retries = retries - 1
        if retries < 0:
            raise ValueError('invalid number')
        print(reminder)
        
    return num


"""
Generates user friendly and efficient input for a yes/no question
"""
def ask_ok(prompt, retries=100, reminder='Please try again!'):
    while True:
        ok = input(prompt)
        if ok in ('y', 'ye', 'yes'):
            return True
        if ok in ('n', 'no', 'nop', 'nope'):
            return False
        retries = retries - 1
        if retries < 0:
            raise ValueError('invalid user response')
        print(reminder)


"""
Allows the user to do some basic calculator operations on two given numbers
"""
def calculator():
    operation_dict = {"1": "Addition", 
                      "2": "Subtraction", 
                      "3": "Multiplication", 
                      "4": "Division"}
    
    num_1 = ask_for_int("Please enter a numerical value: ")
    num_2 = ask_for_int("Please enter a numerical value: ")
            
    print("Would you like to perform: ")    
    for k, v in operation_dict.items():
        print(k, " : " ,v)
        
    operation_k = input("> ") 
    operation_v = operation_dict[operation_k]
    
    result = {
        "1" : lambda x, y: x + y,            
        "2" : lambda x, y: x - y,            
        "3" : lambda x, y: x * y,            
        "4" : lambda x, y: x / y,            
    }[operation_k](num_1, num_2)  
    
    print(operation_v, " of ", num_1, " and ", num_2, " is ", result) 
    
    
"""
Allow the user to re-use the calculator as often they wish
"""    
use_calc = True    
while use_calc:
    calculator()
    use_calc = ask_ok("Would you like to perform another operation y\\n? ")

print("Thank you for using our calculator.")
