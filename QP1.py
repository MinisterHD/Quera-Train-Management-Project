import sys
from os import system

admin_login_creds = {"username": "admin", "password": "1"}
employee_list = {}
registered_emails = []
users_list = {}
lines_list = {}
trains_list = {}
last_state_list = []
current_user = {"name": "", "type": ""}


def admin_login(username, password):
    global current_user
    try:
        if username == admin_login_creds["username"] and password == admin_login_creds["password"]:
            current_user = {"name": username, "type": "Admin"}
            return True
        else:
            return False
    except:
        return False


def employee_login(username, password):
    try:
        global current_user
        if employee_list[username].password == password:
            current_user = {"name": username, "type": "Employee"}
            return True
        else:
            return False
    except:
        return False


def user_login(username, password):
    try:
        global current_user
        if users_list[username].password == password:
            current_user = {"name": username, "type": "User"}
            return True
        else:
            return False
    except:
        return False


class Employee:
    def __init__(self, name, last_name, email, username, password):
        self.name = name
        self.last_name = last_name
        self.email = email
        self.username = username
        self.password = password

    def add_line(self, name, start, end, stops_count, stops_list):
        if name in lines_list.keys():
            print("Line name already exists.")
            return False
        lines_list[name] = Line(start, end, stops_count, stops_list)
        print(f"Line {name} added successfully.")
        return True

    def del_line(self, name):
        if name not in lines_list:
            print("Line not found.")
            return False
        del lines_list[name]
        print(f"Line {name} deleted successfully.")
        return True

    def list_lines(self):
        if not lines_list:
            print("No lines found.")
        for name, line in lines_list.items():
            print(
                f"Name: {name}, Start: {line.start}, End: {line.end}, Stops Count: {line.stops_count}, Stops List: {line.stops_list}"
            )

    def train_accident_detection(self, id, name, line, avg_speed, stop_time, quality_class, ticket_price, capacity):
        avg_speed_list = [train.avg_speed for train in trains_list.values() if train.line == line]
        line_avg_speed = (sum(avg_speed_list) + avg_speed) / (len(avg_speed_list) + 1)
        number_of_trains = len(avg_speed_list)
        line_stops = lines_list[line].stops_count
        avg_waiting_list = [train.stop_time for train in trains_list.values() if train.line == line]
        avg_waiting_time = (sum(avg_waiting_list) + stop_time) / (len(avg_waiting_list) + 1)
        line_length = (line_stops - 1) * 3
        loop_lengh = 2 * line_length
        if loop_lengh / (line_avg_speed * number_of_trains) < 3 * (avg_waiting_time / 60):
            print(
                " train was not added ... \n adding this train may cause accidents in this line ! \n please consider lowering the speed or stop time"
            )
            return True
        return False

    def add_train(self, id, name, line, avg_speed, stop_time, quality_class, ticket_price, capacity):
        if id in trains_list.keys():
            print("Train id already exists.")
            return False
        if self.train_accident_detection(id, name, line, avg_speed, stop_time, quality_class, ticket_price, capacity):
            print("Adding this train will cause accident")
            return False
        trains_list[id] = Train(id, name, line, avg_speed, stop_time, quality_class, ticket_price, capacity)
        print(f"Train with id {id} added successfully.")
        return True

    def del_train(self, id):
        if id not in trains_list:
            print("Train not found.")
            return False
        del trains_list[id]
        print("Train deleted successfully.")
        return True

    def list_train(self):
        if not trains_list:
            print("No trains found.")
        for id, train in trains_list.items():
            print(
                f"id:{id},Name: {train.name}, Line: {train.line}, Avg Speed: {train.avg_speed}, Stop Time: {train.stop_time}, Quality: {train.quality_class}, Ticket Price: {train.ticket_price}, Capacity: {train.capacity}"
            )


class User:
    def __init__(self, name, last_name, email, username, password):
        self.name = name
        self.last_name = last_name
        self.email = email
        self.username = username
        self.password = password
        self.credit = 0
        pass

    def add_credit(self, amount):
        self.credit += amount


class Line:
    def __init__(self, start, end, stops_count, stops_list):
        self.start = start
        self.end = end
        self.stops_count = stops_count
        self.stops_list = stops_list


class Train:
    def __init__(self, id, name, line, avg_speed, stop_time, quality_class, ticket_price, capacity):
        self.name = name
        self.line = line
        self.avg_speed = avg_speed
        self.stop_time = stop_time
        self.quality_class = quality_class
        self.ticket_price = ticket_price
        self.capacity = capacity
        self.remaining_capacity = capacity
        self.id = id
        pass


def display_menu(menu):
    for k, function in menu.items():
        print(k, function.__name__)


def admin():
    print("You are in admin page, choose an action to continue...")

    def Add_Employee():
        print("You Want to Add an Employee")
        name = input("please enter the name or 0 to return ")
        if name == "0":
            main()
        last_name = input("please enter the last_name or 0 to return ")
        if last_name == "0":
            main()

        while True:
            username = input("please enter the username or 0 to return ")
            if username == "0":
                main()
            if username in employee_list.keys():
                print("The username you entered is already taken. Please choose a different username: ")
            else:
                break
        password = input("please enter the password or 0 to return ")
        if password == "0":
            main()
        while True:
            email = input("please enter the email or 0 to return ")
            if email == "0":
                main()
            if email in registered_emails:
                print("This email has been registered before, try again  ")
            else:
                break
        employee_list.update({username: Employee(name, last_name, email, username, password)})
        registered_emails.append(email)
        input("employee was added successfully, please press enter to return to admin menu ...")
        admin()

    def Del_Employee():
        print("You Want to Remove an Employee")
        while True:
            username = input("Enter the username to remove or 0 to return to admin menu")
            if username == "0":
                admin()
            if username in employee_list.keys():
                registered_emails.remove(employee_list[username].email)
                employee_list.pop(username)
                break
            else:
                print("username not found. please try again ...")
        input("employee was removed successfully, please press enter to return to admin menu ...")
        admin()

    def Employee_List():
        print("You Want to See the Employee List")

        if not employee_list:
            print("No employee found.")
        else:
            for username, emp in employee_list.items():
                print(
                    f"username: {username}, name: {emp.name}, last name: {emp.last_name}, email: {emp.email}, password: {emp.password}"
                )
        input("please press enter to return to admin menu ...")
        admin()

    def Admin_Exit():
        input("You have Logged Out successfully, press enter to return to main menu ...")
        main()

    Sub_functions_names = [Add_Employee, Del_Employee, Employee_List, Admin_Exit]
    Sub_menu_items = dict(enumerate(Sub_functions_names, start=1))
    display_menu(Sub_menu_items)
    while True:
        try:
            selection = int(input("Please enter your selection number or 0 to return: "))
            if selection < 5:
                break
            else:
                print("Invalid.Please enter your selection number again: ")
        except:
            print("invalid input. please enter a vaild number ...")
    if selection == 0:
        main()
    selected_value = Sub_menu_items[selection]
    selected_value()


def employee():
    print("you have entered as an employee, choose an action to continue...")

    def Add_Line():
        print("Adding a new line")
        name = input("enter the line name or enter 0 to return to employee menu")
        if name == "0":
            employee()
        start = input("enter the starting position or enter 0 to return to employee menu ")
        if start == "0":
            employee()
        end = input("enter the destination or enter 0 to return to employee menu")
        if end == "0":
            employee()
        while True:
            try:
                stops_count = int(input("enter the number of stops or 0 to return to employee menu "))
                break
            except:
                print("Please Enter a Valid Number")
        if stops_count == 0:
            employee()
        stops_list = [start]
        for i in range(stops_count - 2):
            next_step = input(f"enter the next station. {stops_count-i-2} stations remaining . or 0 to return to employee menu ")
            if next_step == "0":
                employee()
            stops_list.append(next_step)
        stops_list.append(end)
        current_employee_name = current_user["name"]
        current_employee = employee_list[current_employee_name]
        current_employee.add_line(name, start, end, stops_count, stops_list)
        input("press enter to return to employee menu ...")
        employee()

    def Update_Line():
        global lines_list
        print("You Want To Update a Line")
        while True:
            a = input("give the name of the line you want to edit or enter 0 to return to employee menu ")
            if a == "0":
                employee()
            try:
                line = lines_list[a]
                print(
                    f"Name: {a}, Start: {line.start}, End: {line.end}, Stops Count: {line.stops_count}, Stops List: {line.stops_list}"
                )
                break
            except:
                print("not found,enter again")
        while True:
            b = input(
                "press\n 1 to edit name \n 2 to edit start \n 3 to edit end \n 4 to edit number of stops \n 5 to edit list of stops \n 0 to return\n choose one :"
            )
            if b in ["0", "1", "2", "3", "4", "5"]:
                break
            else:
                print("invalid selection. try again")
        if b == "1":
            new_name = input("please enter new start name or enter 0 to return to update line menu ")
            if new_name == "0":
                Update_Line()
            line_values = lines_list[a]
            lines_list[new_name] = line_values
            lines_list.pop(a)
        elif b == "2":
            new_name = input("please enter new start name or enter 0 to return to update line menu ")
            if new_name == "0":
                Update_Line()
            lines_list[a].start = new_name
            lines_list[a].stops_list[0] = new_name
            print(
                f"Name: {a}, Start: {line.start}, End: {line.end}, Stops Count: {line.stops_count}, Stops List: {line.stops_list}"
            )
        elif b == "3":
            new_name = input("please enter new end name or enter 0 to return to update line menu ")
            if new_name == "0":
                Update_Line()
            lines_list[a].end = new_name
            lines_list[a].stops_list[line.stops_count - 1] = new_name
            print(
                f"Name: {a}, Start: {line.start}, End: {line.end}, Stops Count: {line.stops_count}, Stops List: {line.stops_list}"
            )
        elif b == "4":
            while True:
                try:
                    new_count = int(input("please enter new number of stops or enter 0 to return to update line menu "))
                    if new_count == 0:
                        Update_Line()
                    if new_count < 2:
                        print("number of stops should be bigger than two ! ")
                    else:
                        break
                except:
                    print("please enter a number")

            stops_list = [line.start]
            for i in range(new_count - 2):
                next_step = input(
                    f"enter the next station. {new_count-i-2} stations remaining or enter 0 to return to update line menu "
                )
                if next_step == "0":
                    Update_Line()
                stops_list.append(next_step)

            stops_list.append(line.end)

            lines_list[a].stops_count = new_count
            line.stops_list = stops_list
            print(
                f"Name: {a}, Start: {line.start}, End: {line.end}, Stops Count: {line.stops_count}, Stops List: {line.stops_list}"
            )
        elif b == "5":
            print(f"your line has {lines_list[a].stops_count} stops. please enter {lines_list[a].stops_count - 2} names")
            for k in range(1, lines_list[a].stops_count - 1):
                new_name = input(f"please enter new name of stop number {k} or enter 0 to return to update line menu ")
                if new_name == "0":
                    Update_Line()
                lines_list[a].stops_list[k] = new_name
            print(
                f"Name: {a}, Start: {line.start}, End: {line.end}, Stops Count: {line.stops_count}, Stops List: {line.stops_list}"
            )
        elif b == "0":
            employee()
        input("your line was updated. press enter to return to update line menu ...")
        Update_Line()

    def Delete_Line():
        print("You Want To Delete a Line")
        current_employee_name = current_user["name"]
        current_employee = employee_list[current_employee_name]
        while True:
            line_name = input("enter the line name to delete or 0 to return to employee menu")
            if line_name == "0":
                employee()
            if current_employee.del_line(line_name):
                break
            else:
                print("invalid line name, Try again")
        input("press enter to return to delete line menu ...")
        Delete_Line()

    def list_of_lines():
        current_employee_name = current_user["name"]
        current_employee = employee_list[current_employee_name]
        print("Printing the list of lines ...")
        current_employee.list_lines()
        input("press enter to return to previous menu ...")
        employee()

    def Add_Train():
        print("You Want To Add a Train")
        current_employee_name = current_user["name"]
        current_employee = employee_list[current_employee_name]
        while True:
            id = input("please enter id or enter 0 to return")
            if id == "0":
                employee()
            if id in trains_list.keys():
                print("invalid id, please try again")
            else:
                break
        name = input("please enter name or enter 0 to return")
        if name == "0":
            employee()
        while True:
            line = input("please enter line or enter 0 to return")
            if line == "0":
                employee()
            if line in lines_list.keys():
                break
            else:
                print("invalid line name, try again")
        while True:
            try:
                avg_speed = float(input("please enter average speed in km/s or enter 0 to return"))
                if avg_speed == 0:
                    employee()
                if avg_speed > 0:
                    break
                else:
                    print("please enter a positive value")
            except:
                print("please enter a valid number")

        while True:
            try:
                stop_time = float(input("please enter stop time in minutes or enter 0 to return"))
                if stop_time == 0:
                    employee()
                if stop_time > 0:
                    break
                else:
                    print("please enter a positive value")
            except:
                print("please enter a valid number")

        quality_class = input("please enter quality_class or enter 0 to return")
        if quality_class == "0":
            employee()

        while True:
            try:
                ticket_price = float(input("please enter ticket price or enter 0 to return"))
                if ticket_price == 0:
                    employee()
                if ticket_price > 0:
                    break
                else:
                    print("please enter a positive value")
            except:
                print("please enter a valid number")

        while True:
            try:
                capacity = int(input("please enter capacity or enter 0 to return"))
                if capacity == 0:
                    employee()
                if capacity > 0:
                    break
                else:
                    print("please enter a positive value")
            except:
                print("please enter a valid number")
        if current_employee.add_train(id, name, line, avg_speed, stop_time, quality_class, ticket_price, capacity):
            pass
        else:
            input("press enter to try again ... ")
            Add_Train()
        input("press enter to return to employee menu ...")
        employee()

    def Delete_Train():
        print("You Want To Delete a Train")
        current_employee_name = current_user["name"]
        current_employee = employee_list[current_employee_name]
        while True:
            id = input("Enter the id of the train you want to delete: ")
            if id in trains_list.keys():
                current_employee.del_train(id)
                break
            else:
                print("invalid train id, try again ...  ")
        input("press enter to return to previous menu ...")
        employee()

    def Train_List():
        print("You Want To See The Full List of Trains")
        current_employee_name = current_user["name"]
        current_employee = employee_list[current_employee_name]
        current_employee.list_train()
        input("press enter to return to previous menu ...")
        employee()

    def Employee_Exit():
        input("You have Logged Out successfully, press enter to return to main menu ...")
        main()

    Sub_functions_names = [Add_Line, Update_Line, Delete_Line, list_of_lines, Add_Train, Delete_Train, Train_List, Employee_Exit]
    Sub_menu_items = dict(enumerate(Sub_functions_names, start=1))
    display_menu(Sub_menu_items)
    while True:
        try:
            selection = int(input("Please enter your selection number or 0 to return: "))
            if selection < 9:
                break
            else:
                print("Invalid.Please enter your selection number again: ")
        except:
            print("invalid input. please enter a vaild number ...")
    if selection == 0:
        main()
    selected_value = Sub_menu_items[selection]
    selected_value()


def admin_login_page():
    print("you have selected admin, please Enter your Username and Password")
    username = input("please Enter Your Username or 0 to return ")
    if username == "0":
        main()
    password = input("please Enter Your Password or 0 to return ")
    if password == "0":
        main()
    if admin_login(username, password):
        admin()
    else:
        print("Try Again")
        admin_login_page()


def employee_login_page():
    print("you have selected Employee login page ,please Enter your Username and Password")
    username = input("please Enter Your Username or 0 to return ")
    if username == "0":
        main()
    password = input("please Enter Your Password or 0 to return ")
    if password == "0":
        main()
    if employee_login(username, password):
        employee()
    else:
        print("Try Again")
        employee_login_page()


def user_login_page():
    print("you have selected User ,please Enter your Username and Password")
    username = input("please Enter Your Username or 0 to return ")
    if username == "0":
        main()
    password = input("please Enter Your Password or 0 to return ")
    if password == "0":
        main()
    if user_login(username, password):
        user()
    else:
        print("Try Again")
        user_login_page()


def user_signup_page():
    print("registering a new user ...")
    name = input("please enter your name or 0 to return")
    if name == "0":
        main()
    last_name = input("please enter your last name or 0 to return")
    if last_name == "0":
        main()
    while True:
        email = input("please enter your email or 0 to return")
        if email == "0":
            main()
        if email in registered_emails:
            print("this email is already in use, please use another one ")
        else:
            break

    while True:
        username = input("please enter your username or 0 to return")
        if username == "0":
            main()
        if username in users_list.keys():
            print("this username is already taken, please choose another one ")
        else:
            break

    password = input("please enter your password or 0 to return")
    if password == "0":
        main()
    users_list[username] = User(name, last_name, email, username, password)
    registered_emails.append(email)
    print(f"user {username} was added. please login to continue")
    input("press enter to go to login page ...")
    user_login_page()


def user():
    print("you have selected User")

    def add_credit():
        global current_user
        current_user_name = current_user["name"]
        current_end_user = users_list[current_user_name]
        print(f"your current credit: {current_end_user.credit}")
        while True:
            try:
                amount = int(input("how much money you want to deposit or enter 0 to return to main "))
                if amount < 0:
                    print("please enter a positive number")
                else:
                    break
            except:
                print("please enter a number")
        if amount == 0:
            main()
        current_end_user.add_credit(amount)
        print(f"your new credit: {current_end_user.credit}")

        input("press enter to go to previous menu ...")
        user()

    def buy_ticket():
        global current_user
        current_user_name = current_user["name"]
        current_end_user = users_list[current_user_name]
        print("your want to buy a ticket")
        train_names = [{train.name: train.id} for train in trains_list.values()]
        print(f"list of trains and their id: {train_names}")
        while True:
            train_id = input("enter id of train or 0 to return to main menu")
            if train_id == "0":
                main()
            if train_id in trains_list.keys():
                break
            else:
                print("please enter a valid id")
        while True:
            try:
                number_of_tickets = int(
                    input(
                        f"this train has {trains_list[train_id].remaining_capacity} empty seats \n and price of each seat is {trains_list[train_id].ticket_price} \n and your credit is {current_end_user.credit} \n enter number of tickets you want or 0 to return"
                    )
                )

                if number_of_tickets == 0:
                    main()
                if number_of_tickets > trains_list[train_id].remaining_capacity:
                    print("not enough capacity")
                elif number_of_tickets * trains_list[train_id].ticket_price > current_end_user.credit:
                    print("you dont have enough credit. please buy some or choose a lower number of tickets")
                else:
                    current_end_user.credit -= number_of_tickets * trains_list[train_id].ticket_price
                    trains_list[train_id].remaining_capacity -= number_of_tickets
                    print(
                        f"now you have {number_of_tickets} tickets for train with name :{trains_list[train_id].name} and id: {trains_list[train_id].id} in line : {trains_list[train_id].line} and class : {trains_list[train_id].quality_class} \n and your new credit is {current_end_user.credit}"
                    )
                    break
            except:
                print("please enter a number")
        input("press enter to go to user menu ...")
        user()

    def edit_profile():
        global current_user
        current_user_name = current_user["name"]
        current_end_user = users_list[current_user_name]
        print("editing your profile ...")
        print(
            f"your currecnt profile: name: {current_end_user.name} last name: {current_end_user.last_name} email: {current_end_user.email} username: {current_end_user.username} password: {current_end_user.password} remaining credit: {current_end_user.credit}"
        )
        selection = input(
            f"press \n1 to edit your name \n2 to edit your last name \n3 to edit your email \n4 to edit your username \n5 to edit your password \n0 to return\n "
        )
        if selection == "0":
            user()
        if selection == "1":
            name = input("please enter your new name or 0 to return to user menu ")
            if name == "0":
                user()
            current_end_user.name = name
        if selection == "2":
            lastname = input("please enter your new last name or 0 to return to user menu ")
            if lastname == "0":
                user()
            current_end_user.last_name = lastname
        if selection == "3":
            email = input("please enter your new email or 0 to return to user menu ")
            if email == "0":
                user()
            registered_emails.remove(current_end_user.email)
            registered_emails.append(email)
            current_end_user.email = email
        if selection == "4":
            while True:
                new_username = input("please enter your new username or 0 to return to user menu ")
                if new_username == "0":
                    user()
                if new_username in users_list.keys():
                    print("this username is already taken, please choose another one ")
                else:
                    users_list[new_username] = current_end_user
                    users_list[new_username].username = new_username
                    users_list.pop(current_user_name)
                    input("username changed. please login again ...")
                    main()
        if selection == "5":
            password = input("please enter your new password or 0 to return")
            if password == "0":
                user()
            current_end_user.password = password
        print(
            f"your new profile: name: {current_end_user.name} last name: {current_end_user.last_name} email: {current_end_user.email} username: {current_end_user.username} password: {current_end_user.password} remaining credit: {current_end_user.credit}"
        )
        input("press enter to go to previous menu ...")
        user()

    def user_exit():
        input("You have Logged Out successfully, press enter to return to main menu ...")
        main()

    Sub_functions_names = [add_credit, buy_ticket, edit_profile, user_exit]
    Sub_menu_items = dict(enumerate(Sub_functions_names, start=1))
    display_menu(Sub_menu_items)
    while True:
        try:
            selection = int(input("Please enter your selection number or 0 to return to main menu: "))
            if selection < 5:
                break
            else:
                print("Invalid.Please enter your selection number again: ")
        except:
            print("invalid input. please enter a vaild number ...")
    if selection == 0:
        main()
    selected_value = Sub_menu_items[selection]
    selected_value()


def Exit():
    print("Goodbye")


def main():
    functions_names = [admin_login_page, employee_login_page, user_signup_page, user_login_page, Exit]
    menu_items = dict(enumerate(functions_names, start=1))
    display_menu(menu_items)
    while True:
        try:
            selection = int(input("Please enter your selection number: "))
            if selection < 6:
                break
            else:
                print("Invalid.Please enter your selection number again: ")
        except:
            print("invalid input. please enter a vaild number ...")
    if selection == 0:
        main()
    selected_value = menu_items[selection]
    selected_value()


employee_list = {"u1": Employee("name1", "last_name1", "email1", "u1", "p1")}
users_list["u2"] = User("name1", "last_name1", "email2", "u2", "p2")
registered_emails = ["email1", "email2"]
lines_list["line1"] = Line("start1", "end1", 4, ["start1", "stop1", "stop2", "end1"])
trains_list["1"] = Train("1", "train1", "line1", 30, 1, "First Class", 10, 100)

if __name__ == "__main__":
    main()
