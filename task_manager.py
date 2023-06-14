'''Task 24 - Capstone Project 3 - Lists Functions and String Handling

I got help from my brother. I was struggeling with how to allow the user
to modify their tasks and how to determine if a task is overdue'''

# Import the datetime and date module
from datetime import date
import datetime as dt
# Request the user to enter their username and password
username = input("Enter your username: ")
password = input("Enter your password: ")

# Create variables for the text files
# tasks, user, user_overview and task_overview
task_file = 'tasks.txt'
user_file = 'user.txt'
user_overview_file = 'user_overview.txt'
task_overview_file = 'task_overview.txt'

#deadline_date is the deadline used to determine if tasks are overdue
deadline_date = dt.date.today()
# Save the usernames and passwords from 
# the user text file in a dictionary    
database = {}
with open(user_file, 'r', encoding='utf-8-sig') as f:
    for line in f.readlines():
        user = line.strip().split(', ')[0]
        passwd = line.strip().split(', ')[1]
        database[user] = passwd
    
        
# Create a function to register a user with 2 attributes
# only admin is allowed to register users
# new users are written to the user text file        
def reg_user(user, input_file):
    if menu == 'r' and user == 'admin':
        new_username = input("Enter a new username: ")
        while new_username in database:
            print("\nUser already exists! Try again\n")
            new_username = input("Enter a new username: ")
        new_password = input("Enter a new password: ")
        password_confirm = input("Enter your password again: ")
        if new_password == password_confirm:
            with open(input_file, 'a') as f1:
                f1.write(f"\n{new_username}, {new_password}")
                print(f"\n{new_username} has been registered successfully!\n")        
        else:
            print("\nYour password does not match. Try again\n")
    else:
        print("\nYou are not Admin. You cannot register a user!\n")

# Create a function to add a task with 2 attributes
# each user can add a task
def add_task(user, input_file):
    if menu == 'a':
        user = input("Enter username of task owner: ")
        while user not in database.keys():
            print(" \nYou are not the registerd user. Try again\n")
            user = input("Enter username of task owner: ")
        else:
            title = input("Enter the title of the task: ")
            description = input("Describe the task: ")
            # Convert the date input to short form
            due_date = input("Enter the task due date(dd/mm/yyyy): ")
            mod_date = dt.datetime.strptime(due_date, "%d/%m/%Y").date()
            due_date = dt.datetime.strftime(mod_date, "%d %b %Y")

            current_date = date.today().strftime("%d %b %Y")
            task_complete = 'no'
            with open(input_file, 'a') as f2:
                f2.write(f"\n{user}, {title}, {description}, {current_date}, {due_date}, {task_complete}")

# Create a function with one attribute to view all tasks
# all users have access to this function
# read lines from the tasks text file
# in a userfriendly manner
def view_all(input_file):
     with open(input_file, 'r') as f3:
           for line in f3.readlines():
               info = line.strip().split(", ")
               # display all tasks in a user friendly manner
               print(f'''
   ________________________________________________________________________________________

    Task:               {info[1]}
    Assigned to:        {info[0]}
    Date assigned:      {info[3]}
    Due date:           {info[4]}
    Task Complete?      {info[5]}
    Task description:
    {info[2]}
        ''') 
# Create a function to only view user's tasks
# with 2 attributes

def view_mine(user, input_file):
    if menu == 'vm':
        task_count = 0  # number the tasks
        with open(input_file, 'r') as f4:
            for line in f4.readlines():
                info = line.strip().split(", ")
                if user == info[0]:
                    task_count +=1 
                    # display logged-in user tasks in a user friendly manner
                    print(f'''
   ____________________________________________________________________________________
    
    Task {task_count}:                  {info[1]}
    Assigned to:             {info[0]}
    Date assigned:           {info[3]}
    Due date:                {info[4]}
    Task Complete?           {info[5]}
    Task description:
    {info[2]} 
        ''')
    
    # Create a list of users tasks using the load_task_file function
    task_tbl = []
    task_table = load_task_file(task_tbl, input_file)
    user_task_list = []
    
    # list comprehension to display all tasks assigned to specific user
    pos_user_task_list = [(pos,task) for (pos,task) in enumerate(task_table) if user == task['username']]
    # don't want tuple so that the list can be modified
    user_task_list = [task for task in task_table if user == task['username']]
    
    '''[print(i+1, item) for (i, item) in enumerate(user_task_list)] <-- Items in user_task_list'''
    # Request the user to choose to edit their existing tasks
    selection = input("Select task number to edit or -1 to return to main menu: ")
    selection = int(selection)
    # This takes the user back to the main menu
    if selection == -1:
        pass
    # user selecting a task to modify or complete
    elif selection <= len(user_task_list):
        option = int(input("1 - mark task as complete or \n2 - edit task \nEnter: "))
        # option to mark task as complete
        if option == 1:
            user_task_list[selection-1]['completed'] = 'yes'
            print("\nTask successfully updated to: Complete!\n")
        # only incomplet tasks can be modified
        # user can either leave task unchanged or modify    
        elif option == 2 and user_task_list[selection-1]['completed'] == 'no':
            edit_1 = input("Re-assign to username (Press enter if unchanged): ")
            edit_2 = input("Edit due date dd/mm/yyyy (Press enter if unchanged): ")
            # unchanged username
            edit_1 = edit_1.strip()
            edit_1 = ''.join(edit_1)
            # this ensures username is changed to the new input
            if edit_1 != "":
                user_task_list[selection-1]['username'] = edit_1
                print("\nUsername has been changed successfully!\n")
            # unchanged due date    
            edit_2 = edit_2.strip()
            edit_2 = ''.join(edit_2)
            # this ensures due date is changed to the new input
            # and matches existing date format
            if edit_2 != "":
                mod_date = dt.datetime.strptime(edit_2, "%d/%m/%Y").date()
                edit_2 = dt.datetime.strftime(mod_date, "%d %b %Y")
                user_task_list[selection-1]['due_date'] = edit_2
                print("\nDue date has been changed successfully!\n")
        else:
            print("\nThe task has been completed!\n")    
        # modify original task table with new information
        original_index = pos_user_task_list[selection-1][0]
        task_table[original_index]['completed'] = user_task_list[selection-1]['completed']
        task_table[original_index]['username'] = task_table[original_index]['username']
        task_table[original_index]['due_date'] = task_table[original_index]['due_date']
        
        # write out modified task line to file
        with open(input_file, "w") as f5:
            for lines in task_table:
                value_list = list(lines.values())
                f5.write(', '.join(value_list))
                f5.write('\n')

    else:
        print("\nSelected task number does not correspond to an assigned task \n")        
  

# Create a function with 2 variables
# to load the task file as a list of dictionaries
# this function was used earlier
def load_task_file(task_table, input_file):
    task_headings = ["username", "title", "description",
                     "assignment_date", "due_date", "completed"]

    # task_table = []

    # convert task.txt to list of dictionary itmes
    # with each list entry representing a new line of tasks
    # and each dictionary item representing a task property
    # this categorization of the data makes it easier to 
    # summarize
    with open(input_file, "r") as f6:
        
        for line in f6.readlines():
            task_dict = {}
            due_date = []
            assign_date = []
            entry = line.strip().split(', ')
            # convert zipped file back to dictionary
            task_dict = dict(zip(task_headings, entry))
            # format dates
            due_date = task_dict['due_date'].split()
            assign_date = task_dict['assignment_date'].split()

            # only take the first 3 letters in the month
            # this is important to ensure date format
            # is correct when converting date string
            # to actual date
            due_date[1] = due_date[1][:3]
            str_due_date = ' '.join(due_date)
            task_dict['due_date'] = str_due_date
            
            assign_date[1] = assign_date[1][:3]
            str_assign_date = ' '.join(assign_date)
            task_dict['assignment_date'] = str_assign_date
            
            # format completion status to lower case
            # for ease of comparisons
            task_dict['completed'] = task_dict['completed'].lower()
            task_table.append(task_dict)
                
        return task_table
    
# Create a function for the task overview output file
# with 3 attributes
def write_task_overview(task_table, cutoff_date, output_file):
    # contains overall report information
    # cutoff_date is the deadline used to determine if tasks are overdue
    
    # total number of tasks across all users
    total_tasks = len(task_table)
    
    # using list_comprehension to display all
    # task completion statuses for all users
    total_completion_list = [task['completed'] for task in task_table]

    # using list_comprehension to display all
    # task titles of incomplete and overdue tasks 
    # for all users
    total_incomplete_overdue_tasks = [task['title'] for task in task_table if cutoff_date > dt.datetime.strptime(task['due_date'], '%d %b %Y').date() and task['completed'] == 'no']

    # using list_comprehension to display all
    # task titles of overdue tasks for all users
    total_overdue_tasks = [task['title'] for task in task_table if cutoff_date > dt.datetime.strptime(task['due_date'], '%d %b %Y').date()]

    # number of (in)complete tasks for all users
    total_complete_count = total_completion_list.count('yes')
    total_incomplete_count = total_completion_list.count('no')

    # number of overdue and incomplete tasks for all users
    total_incomplete_overdue_count = len(total_incomplete_overdue_tasks)

    # number of overdue tasks for all users
    total_overdue_count = len(total_overdue_tasks)

    # proportion of all users tasks that are still incomplete
    total_incomplete_portion = total_incomplete_count/total_tasks
   
    # proportion of all users tasks that are overdue
    total_overdue_portion = total_overdue_count/total_tasks

    # write out report to task_overview.txt
    # in user friendly manner
    with open(output_file, 'w') as f7:
        f7.write(f'''
 __________________________________________________________________________________________________________
Total number of tasks tracked:                 {total_tasks}
Total number of completed tasks:               {total_complete_count}
Total number of uncompleted tasks:             {total_incomplete_count}
Total number of incomplete and overdue tasks:  {total_incomplete_overdue_count}
Percentage of incomplete tasks:                {round(total_incomplete_portion*100,2)}%
Percentage of overdue tasks:                   {round(total_overdue_portion*100,2)}%
\n''')
                        
# Create a user overview function with
# 4 attributes
def write_user_overview(user, task_table, cutoff_date, output_file):
    # it contains user-specific report information
    # user = 'admin'
    # cutoff_date is the deadline used to determine if tasks are overdue
    
    user_list = []
    
    # using list_comprehension to display all usernames
    user_list = [task['username'] for task in task_table]
    # remove duplicate usernames
    user_list = list(set(user_list))
    
    # total number of registered users with tasks
    total_no_users = len(user_list)

    tracked_users = []
    
    if user == 'admin':
        tracked_users = user_list
    else:
        print("\nYou do not have access to this feature\n")
    
    #clear user_overview.txt
    with open(output_file, 'w') as f8:
        f8.write('')
        
        
    for member in tracked_users:

        user_completion_list = []
      
        # total number of tasks across all users
        total_tasks = len(task_table)

        # using list_comprehension to display all
        # task completion statuses for the user
        user_completion_list = [task['completed'] for task in task_table if task['username'] == member]

        '''
        #using list_comprehension to display all
        #task due dates for the user
        user_due_date_list = [task['due_date'] for task in task_table if task['username'] == member]

        #using list_comprehension to display all
        #task titles of overdue tasks for the user
        user_overdue_tasks = [task['title'] for task in task_table if task['username'] == member and cutoff_date > dt.datetime.strptime(task['due_date'], '%d %b %Y').date()]
        '''
        # using list_comprehension to display all
        # task titles of incomplete and overdue tasks 
        # for the user
        user_incomplete_overdue_tasks = [task['title'] for task in task_table if task['username'] == member and cutoff_date > dt.datetime.strptime(task['due_date'], '%d %b %Y').date() and task['completed'] == 'no']

        # total number of tasks assigned to specific user
        user_total_tasks = len(user_completion_list)

        # user's share of all assigned tasks
        user_task_portion = user_total_tasks/total_tasks

        #number of (in)complete tasks for user
        user_complete_count = user_completion_list.count('yes')
        user_incomplete_count = user_completion_list.count('no')

        # number of overdue and incomplete tasks for user
        user_incomplete_overdue_count = len(user_incomplete_overdue_tasks)
        
        # proportion of user's tasks that have been completed
        if user_total_tasks == 0:
            user_complete_portion = 0
        else:
            user_complete_portion = user_complete_count/user_total_tasks

        # proportion of user's tasks still incomplete
        if user_total_tasks == 0:
            user_incomplete_portion = 0
        else:
            user_incomplete_portion = user_incomplete_count/user_total_tasks

        # proportion of user's tasks that are incomplete 
        # and overdue
        if user_total_tasks == 0:
            user_incomplete_overdue_portion = 0
        else:
            user_incomplete_overdue_portion = user_incomplete_overdue_count/user_total_tasks
       
        # write out report to user_overview.txt
        # for users in task table:
    
        with open(output_file, 'a') as f8:
            f8.write(f'''
___________________________________________________________________________________________________________
Total number of users registered:                          {total_no_users}
Total number of tasks tracked:                             {total_tasks}
Username:                                                  {member}
Total number of tasks assigned to user:                    {user_total_tasks}
Proportion of total number of tasks assigned to user:      {round(user_task_portion*100,2)}%
Percentage of user-specific tasks completed:               {round(user_complete_portion*100,2)}%
Percentage of user-specific tasks uncompleted:             {round(user_incomplete_portion*100,2)}%
Percentage of user-specific tasks uncompleted and overdue: {round(user_incomplete_overdue_portion*100,2)}%
\n''')
              
            

logged_in = False
while(username != database.keys() and password != database.get(username)):
        print("Sorry, username and password is incorrect. Try again")
        username = input("Enter your username: ")
        password = input("Enter your password: ")  
else:
    print(f"\nWelcome {username}\n")
    logged_in = True 
 
while logged_in == True:
    if username == 'admin':
        menu = input(''' Select one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my task
gr - Generate reports
ds - Display statistics
e - Exit
: ''').lower()
    else:
        menu = input(''' Select one of the following Options below:
r - Registering a user (Admin only)
a - Adding a task
va - View all tasks
vm - View my task
e - Exit
 ''').lower()
                   
    # task_file = 'tasks.txt'
    # user_file = 'user.txt'
    task_tbl = []
    if menu == 'r':
        # user_file = 'user.txt'
        reg_user(username, user_file)
                
    elif menu == 'a':
        # task_file = 'tasks.txt'
        add_task(username, task_file)
        # load_task_file(task_tbl, task_file)
    
    elif menu == 'va':
        # task_file = 'tasks.txt'
        view_all(task_file)
                                          
    elif menu == 'vm':
        # task_file = 'tasks.txt'
        view_mine(username, task_file)
                
    elif menu == 'gr':
        # initialize list that will contail all tasks contained in the task file
        # task_tbl = []
        # load task list into the program
        # task_file = "tasks.txt"
        # only admin can generate report
        out_task_tbl = load_task_file(task_tbl, task_file)

        # write user overview report to file
        # user_overview_file = 'user_overview.txt'
        # username == 'admin'
        write_user_overview(username, out_task_tbl, deadline_date, user_overview_file)
        print('User overview txt report has been generated')
        
        # write task overview report to file
        # task_overview_file = 'task_overview.txt'
        write_task_overview(out_task_tbl, deadline_date, task_overview_file)
        print('Task overview txt report has been generated')
        
    # only admin can display stats   
    elif menu == 'ds' and username == 'admin':
        # write user overview report to menu/screen
        # user_overview_file= 'user_overview.txt'
        print('\n\nDue date for tasks: {}'.format(deadline_date))
        with open(user_overview_file, 'r') as f9:
            for line in f9.readlines():
                print(line)
               
            
        # display task overview report to screen
        # task_overview_file = 'task_overview.txt'
        # deadline date reminds user
        print('\n\nDue date for tasks: {}'.format(deadline_date))
        with open(task_overview_file, 'r') as f10:
            for line in f10.readlines():
                print(line)
                         

                           
    elif menu == 'e':
        print('Goodbye!!!')
        exit()

    else:
        print("\nYou have made a wrong choice, Please Try again\n")

            