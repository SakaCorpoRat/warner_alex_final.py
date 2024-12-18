import argparse
import os

# This was by far the most challanging thing that I have ever written but I really pushed myself on this one to try and use soem more complex stuff
# which definately didnt make this any easier lol
# It took my days to get it to where it is now but I feel like I did a pretty good job
# I think that it could use soem refinement and polishing but in its currents state it works
# I tried soem new things and spent alot of time trying to get this to where I felt it was usable
# I wanted to add a way to remove items but i unfortunately ran out of time
# Also I have this set up where by default the program will write to TODO.txt unless otherwise specified using the --list command

# defines the default todo file
default_todo = "TODO.txt"

# stores the list in a list
todo_list = []

# This also took me a little bit and I definately could hav found a less complicated way to do this
# If I remeber correctly this was something off of stack overflow that I had heavely edited
# Loads the list for the tool to use and defines rules for how to sperate and read the different parts of the list by assigning them in parts seperated by '|'
def load_todo_list(file_name):
    if os.path.exists(file_name):
        with open(file_name, "r") as file:
            lines = file.readlines()
            for line in lines:
                parts = line.strip().split('|')
                if len(parts) == 4:
                    todo_list.append({
                        'id': int(parts[0]),
                        'category': parts[1],
                        'description': parts[2],
                        'status': parts[3]
                    })
    else:
        print(f"No existing ToDo list found. A new list will be created.")

# Defines how the list items should be formatted saved
def save_todo_list(file_name):
    with open(file_name, "w") as file:
        for todo in todo_list:
            file.write(f"{todo['id']}|{todo['category']}|{todo['description']}|{todo['status']}\n")
    print(f"ToDo list saved to {file_name}.")

# Some simple code for displaying the list to the user used in the --view command
def display_todos():
    if not todo_list:
        print("No ToDo items found.")
    else:
        for todo in todo_list:
            print(f"[{todo['id']}]\n Category: {todo['category']}\n Description: {todo['description']}\n Status: {todo['status']}\n")

# Logic for how to add new items
# I found it to be alot easier if passing the --add command just triggered promts as opposed to making the user
# type in a bunch of other commands for description, status, etc
# It also automatically adds the ID number acording to how many items are before it on the list
def add_todo_item(file_name):
    category = input("Enter category: ").strip()
    description = input("Enter description: ").strip()
    new_id = len(todo_list) + 1
    new_todo = {
        'id': new_id,
        'category': category,
        'description': description,
        'status': 'incomplete'
    }
    todo_list.append(new_todo)
    save_todo_list(file_name)
    print(f"Added new ToDo item: {new_todo}")

# Oddly enough this gave me more trouble than anything else and I problably spent the most time refining this. However I think that in its current
# state it works relatively well.
def update_todo_item(file_name, todo_id=None, status=None, description=None, category=None):
    if not todo_id:
        try:
            todo_id = int(input("Enter the ID of the TODO item you want to update: ").strip())
        except ValueError:
            print("Invalid ID. Please enter a number.")
            return
        
    # Finds item by ID
    todo_item = next((todo for todo in todo_list if todo['id'] == todo_id), None)
    
    if not todo_item:
        print(f"TODO item with ID {todo_id} not found.")
        return
    
    # Ask the user which part to update
    field_to_update = input("Which part of the TODO item would you like to update? (category, description, status): ").strip().lower()
    
    # Validate the input
    if field_to_update not in ['category', 'description', 'status']:
        print("Invalid field. Please choose from 'category', 'description', or 'status'.")
        return
    
    # Ask the user for the new input
    new_value = input(f"Enter the new {field_to_update}: ").strip()
    
    # Update the field with the new input
    todo_item[field_to_update] = new_value
    save_todo_list(file_name)
    print(f"Updated TODO item {todo_id}: {todo_item}")


# My main logic for the whole program
def main():
    parser = argparse.ArgumentParser(description="Manage your TODO list.")

# CLI Commands
# Found the action='store_true' booleen flag thing when i was running into some issues here but it resolved them
# Sets the default file to the TODO.txt unless otherwise specified
    parser.add_argument('--list', nargs='?', const=default_todo, default=default_todo, help="Specify a TODO list file. (Default is TODO.txt)")
    parser.add_argument('--add', action='store_true', help="Add a new TODO item.")
    parser.add_argument('--update', action='store_true', help="Update an existing TODO item.")
    parser.add_argument('--view', action='store_true', help="View all TODO items.")

    args = parser.parse_args()

# Loads the specified list
    load_todo_list(args.list)

# Some simple logic on how to call the defs above
    if args.view:
        display_todos()
    elif args.add:
        add_todo_item(args.list)
    elif args.update:
        update_todo_item(args.list)
    else:
        print("No valid command provided. Use --help for usage details.")

if __name__ == "__main__":
    main()
