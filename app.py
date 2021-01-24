#########################
# Importing standard python modules
#########################
import time, os

'''
Checking to see if the necessary files are available. 
If one is missing or was renamed, then an error occurs.
'''

#########################
# Importing custom modules
#########################
try:
    from novel_crawlers.syosetu import syosetu_book_grab
    from auxillary_functions import custom_functions
except:
      raise SystemExit("Custom modules could not be imported.")

# Doing the core file check
aux,novel="auxillary_functions","novel_crawlers"
core_files=f"{aux}/custom_functions.py",f"{aux}/yomituki.py",\
           f"{novel}/alphapolis.py",f"{novel}/kakuyomu.py",f"{novel}/syosetu.py"

# if the check fails, then the missing files will be displayed.
core_files_available=custom_functions.system_check(core_files)
if core_files_available[0]==True: pass
else:
    print("The programm could not be started because the core files are missing:\n")
    for file in core_files_available[1]:
        print(file)

#########################
# Importing pip modules
#########################
try:
    import aiohttp,bs4,ebooklib,pykakasi
except Exception as error:
    print(error)
    raise SystemExit

def placeholder():
    print("This function is currently not available")
    input()

def contribution_license():
    with open ("documentation/LICENSE") as license:
        for line in license:
            print(line.strip())
    input("Please press enter to return to the main menu:")

#########################
# The Main Menu Function
#########################
def run_program():
     menu_option = {"Version History":placeholder,
                    "Contribution and license":contribution_license,
                    "Programm documentation":placeholder,
                    "Syosetu": syosetu_book_grab,
                    "Kakuyomu":placeholder,
                    "Alphapolis":placeholder}

     invalid_option = "An error has occurred. Press enter to return to the main menu"

     while True:
         while True:
            banner = "Japanese Web Novel Crawler Version 1.0", "Main Menu"
            for word in banner:
                print(word.center(40,"~"))
            print("\n- The function names are not case-sensistive - \n")
            for num, elem in enumerate(menu_option, start=1):
                print(f'{num}: {elem}')

            choice_str = input('\nPlease enter the name or number of the function: ').strip()
            options_func_dict = menu_option.get(choice_str.title())

            if options_func_dict:
                break
            else:
                try:
                     choice_num = int(choice_str)
                except Exception as error:
                     print(error)
                     input(invalid_option)
                else:
                     if 0 < choice_num and choice_num <= len(menu_option):
                         func_list = list(menu_option.values())
                         function_number = choice_num - 1
                         options_func_dict = func_list[function_number]
                         options_func_dict()
                     else:
                          input(invalid_option)

################ Calling App.py ################

if __name__ == "__main__":
     if core_files_available[0]==True:
        try:
            run_program()
        except Exception as error:
            print(error)
