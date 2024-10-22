# Lir-Wan Fan
# Purpose: Creating a Pets Class using different inputs and values
# 1. Start
# 2. Connect to your personal (pets) database
# 3. Read data
# 4. Create one (object) instance of a Pets class for each pet listed in your database.
#     Keep your Pets class in a separate file
# 5. Display a list of pet names, from the pet object instances
# 6. Ask the user to choose a pet
# 7. Once a pet is chosen, print that pet's info from the (object) instance.
####################################################################################

# 1. Start
# Importing pymysql.cursors
import pymysql.cursors

# Contain your database credentials
from creds import *

# 2. Creating a connection to the MySQL database
try:
    myConnection = pymysql.connect(
        host=hostname,
        user=username,
        password=password,
        db=database,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    print("Database connection established.")

# If any error occurs, it will stored as e, and print the error message and exit the program.
except Exception as e:
    print(f"Error connecting to the database.  Exiting: {e}")
    exit()

# 4. Creating another python file named pet_class.py.  Importing PetsClass from this separate file.
from pets_class import PetsClass

# 3. Read data.  Creating a list of Pets Class instances based on the data fetched from the database.
pets_list = []

try:
    with myConnection.cursor() as cursor:
        # Modify the SQL query to perform a LEFT JOIN to include pets without matching owners
        sqlSelect = """
            SELECT pets.name, types.animal_type as types_animal_type, pets.age, owners.name as owner_name
            FROM pets
            LEFT JOIN owners ON pets.owner_id = owners.id
            LEFT JOIN types ON pets.animal_type_id = types.id;
        """
        cursor.execute(sqlSelect)

        # Fetch all results at once
        rows = cursor.fetchall()

        if not rows:
            print("No pets found in the database.")

        else:
            # Clear the list to avoid duplicates
            pets_list.clear()

            # Create Pets instances
            for row in rows:
                owner_name = row['owner_name'] if row['owner_name'] else "Unknown Owner"  # Handle NULL owner
                types_animal_type = row['types_animal_type'] if row['types_animal_type'] else "Unknown Type"  # Handle NULL Type
                pet = PetsClass(row['name'], types_animal_type, owner_name, row['age'])
                pets_list.append(pet)  # Add to the pets list

except Exception as e:
    print(f"An error occurred while fetching pet data: {e}")

#################################################################################
# 5. Display a list of pet names, from the pet object instances
# 6. Ask the user to choose a pet
def display_pet_choices():
    print("\n################################# Pet Chooser #################################")
    print("Please choose a pet by serial number from the list below or enter 'q' to quit:")
    print("###############################################################################")
    for index, pet in enumerate(pets_list, start=1):
        print(f"[{index}] {pet.name}")

while True:
    # Print Title and Display pet choices
    display_pet_choices()
    print("[Q] Quit")
    user_input = input("Input your choice from the list or enter 'q' to quit:").strip()

    if user_input.lower() == 'q':
        print(f"Thank you very much for using pet chooser.  Exiting the program.  Goodbye!")
        break

    try:
        choice = int(user_input) - 1  # Convert to index

        if 0 <= choice < len(pets_list):
            chosen_pet = pets_list[choice]

# 7. Print the chosen pet's info from the (object) instance.
            print(f"\nYou have chosen {chosen_pet.name}, the {chosen_pet.type}. {chosen_pet.name} is {chosen_pet.age} years old. {chosen_pet.name}'s owner is {chosen_pet.owner}.")
            input("Press [ENTER] to continue.")

        else:
            print("Invalid choice.  Please select a valid number.")

    except ValueError:
        print("Invalid input. Please input a number corresponding to your choice or 'q' to quit.")

# Close the database connection after data is fetched
myConnection.close()
print("Database connection closed.")

