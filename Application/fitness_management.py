import psycopg2
from psycopg2 import Error
import sys
import random
from datetime import datetime, timedelta
import re

# establish a connection to the PostgreSQL database
def create_connection():
    try:
        connection = psycopg2.connect(
            user="postgres",
            password="1312Paimana",
            host="localhost",
            port="5432",
            database="test_db"
        )
        return connection
    except (Exception, Error) as error:
        print("Error connecting to PostgreSQL:", error)
        return None


#ALL MAIN MENUS OF THE PROGRAM: 
 
def start_menu(connection):
    try:
        print("Welcome to the Health and Fitness Club Management System!")
        print("1. Login")
        print("2. Register as a member")
        print("3. Exit")

        choice = input("Enter your choice: ")
        print()

        if choice == "1":
            user_id, user_role = login(connection)
            return user_id, user_role
        elif choice == "2":
            user_id, user_role = register(connection)
            return user_id, user_role
        elif choice == "3":
            print("Exiting the program. Goodbye!")
            sys.exit()
        else:
            print("Invalid choice. Please try again.") 
            print()
            return
    except KeyboardInterrupt:
        print("\nCtrl+C detected. Exiting the program.")
        sys.exit()


def admin_menu(connection):
    print("Welcome, Admin!")
    print("1. Room Booking Management")
    print("2. Equipment Maintenance Monitoring")
    print("3. Class Schedule Updating")
    print("4. Billing and Payment Processing")
    print("5. Logout")

    choice = input("Enter your choice: ")
    print()

    if choice == "1":
        room_booking_management(connection)
    elif choice == "2":
        equipment_maintenance_monitoring(connection)
    elif choice == "3":
        class_schedule_updating(connection)
    elif choice == "4":
        charge_cards(connection)
    elif choice == "5":
        print("Logging out...")
        start_menu(connection)
        
    else:
        print("Invalid choice. Please try again.")
        admin_menu(connection)


def trainer_menu(connection,user_id):
    trainer_id = find_trainer_id(connection, user_id)
    
    print("Welcome, Trainer!")
    print()
    while True:
        print("1. Schedule Management")
        print("2. Member Profile Viewing")
        print("3. Logout")

        choice = input("Enter your choice: ")
        print()

        if choice == "1":
            tschedule_management(connection,trainer_id)
        elif choice == "2":
            member_profile_viewing(connection)
        elif choice == "3":
            print("Logging out...")
            start_menu(connection)
        else:
            print("Invalid choice. Please try again.")


def member_menu(connection, user_id):
    while True:
        print("Welcome, Member!")
        print("1. Profile Management")
        print("2. Dashboard Display")
        print("3. Schedule Management")
        print("4. Logout")

        choice = input("Enter your choice: ")
        print()

        if choice == "1":
            profile_management_menu(connection, user_id)
        elif choice == "2":
            display_dashboard(connection, user_id)
        elif choice == "3":
            schedule_management(connection, user_id)
        elif choice == "4":
            print("Logging out...")
            start_menu(connection)
        else:
            print("Invalid choice. Please try again.")



#LOGIN/REGISTERATION/CREDENTIAL CHECK

 # Handle user login
def login(connection):
    try:
        while True:
            # Prompt user to enter username and password
            print("Enter 'back' to return to the start menu.")
            username = input("Enter your username: ").lower()
            
            if username == "back":
                print("Returning to the start menu.")
                return start_menu(connection)
                
            password = input("Enter your password: ")

            # Check credentials against database
            user_role = check_credentials(connection, username, password)
            if user_role:
                print("Login successful!")
                print()
                return user_role 
            else:
                print("Invalid username or password. Please try again.")
    except KeyboardInterrupt:
        print("\nCtrl+C detected. Exiting the program.")
        sys.exit()


def register(connection):
    print("Please register to continue.")

    # Proceed with registration as a member
    user_type = "member"
    
    # Ask for username and password
    username = input("Enter your desired username: ").lower()
    password = input("Enter your desired password: ")
    weight = float(input("Enter your weight (in pounds): "))
    height = float(input("Enter your height (in feet): "))
    payment_method = input("Enter your payment method (e.g., Credit Card, PayPal): ")
    card_number = input("Enter your card number: ")
    expiration_date = input("Enter your card expiration date (YYYY-MM-DD): ")

    try:
        datetime.strptime(expiration_date, "%Y-%m-%d")
    except ValueError:
        print("Invalid format for expiration date. Please use the format YYYY-MM.")

    try:
        cursor = connection.cursor()

        # Insert into Users table
        cursor.execute("INSERT INTO Users (username, password, user_type) VALUES (%s, %s, %s) RETURNING user_id", (username, password, user_type))
        user_id = cursor.fetchone()[0]
        # Insert into Payments table
        cursor.execute("INSERT INTO Payments (user_id, payment_method, card_number, expiration_date) VALUES (%s, %s, %s, %s)",
                       (user_id, payment_method, card_number, expiration_date))

        # Common user details
        full_name = input("Enter your full name: ")
        email = input("Enter your email: ")
        phone_number = input("Enter your phone number: ")
        address = input("Enter your address: ")
        
        # Select fitness goal
        print("Select your fitness goal:")
        print("1. Lose Weight")
        print("2. Build Muscle")
        print("3. Improve Endurance")
        print("4. Maintain Current Fitness Level")
        choice = input("Enter your choice: ")
        
        fitness_goals = {
            "1": "Lose Weight",
            "2": "Build Muscle",
            "3": "Improve Endurance",
            "4": "Maintain Current Fitness Level"
        }
        
        if choice in fitness_goals:
            fitness_goal = fitness_goals[choice]
        else:
            print("Invalid choice. Setting fitness goal to 'Maintain Current Fitness Level'.")
            fitness_goal = "Maintain Current Fitness Level"

        # Insert into Members table
        cursor.execute("INSERT INTO Members (user_id, full_name, email, phone_number, address, fitness_goal, weight, height) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                       (user_id, full_name, email, phone_number, address, fitness_goal, weight, height))
        
        connection.commit()
        print("Registration successful!")
        member_menu(connection, user_id)
    except psycopg2.Error as error:
        connection.rollback()
        print("Error during registration:", error)
        return False



def check_credentials(connection, username, password):
    try:
        cursor = connection.cursor()

        # Execute SQL query to fetch user information based on username and password
        cursor.execute("SELECT user_id, user_type FROM Users WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()

        if user:
            cursor = connection.cursor()
            user_id, user_type = user

            # Check if the user is a trainer
            if user_type.lower() == "trainer":
                return user_id, "trainer"

            # Check if the user is an admin
            elif user_type.lower() == "admin":
                return user_id, "admin"

            # User is a regular member
            else:
                return user_id, "member"
        else:
            return False # User with provided credentials does not exist
    except psycopg2.Error as error:
        print("Error checking credentials",error)
        return False


#MEMBER FUNCTIONS:

def profile_management_menu(connection, user_id):
    while True:
        print("Profile Management")
        print("1. Update Personal Information")
        print("2. Update Fitness Goals")
        print("3. Update Health Metrics")
        print("4. Go back to Member Menu")

        choice = input("Enter your choice: ")
        print()

        if choice == "1":
            update_personal_info(connection, user_id)
        elif choice == "2":
            update_fitness_goals(connection, user_id)
        elif choice == "3":
            update_health_metrics(connection, user_id)
        elif choice == "4":
            print("Going back to Member Menu...")
            return
        else:
            print("Invalid choice. Please try again.")


def display_dashboard(connection, user_id):
    print("Dashboard Display")
    print("1. Display Exercise Routines")
    print("2. Display Funny Fitness Quote")
    print("3. Display Fitness Achievements")
    print("4. Display Health Statistics")
    print("5. Go back to Member Menu")

    choice = input("Enter your choice: ")
    print()

    if choice == "1":
        display_exercise_routines(connection)
    elif choice == "2":
        display_random_funny_fact(connection)  
    elif choice == "3":
        manage_achievements(connection, user_id)
    elif choice == "4":
        display_health_metrics(connection, user_id)
    elif choice == "5":
        print("Going back to Member Menu...")
        return
    else:
        print("Invalid choice. Please try again.")


def display_health_metrics(connection, user_id):
    try:
        cursor = connection.cursor()

        # Fetch the health metrics for the logged-in member
        cursor.execute("SELECT weight, height FROM Members WHERE user_id = %s", (user_id,))
        health_metrics = cursor.fetchone()

        if health_metrics:
            weight, height = health_metrics
            print("Current Health Metrics:")
            print(f"Weight: {weight} pounds")
            print(f"Height: {height} feet")
            print()
        else:
            print("Health metrics not found for the current member.")

    except psycopg2.Error as error:
        print("Error fetching health metrics:", error)

    member_menu(connection, user_id)


# Function to allow member to add an achievement
def add_achievement(connection, user_id):
    achievement_description = input("Enter your achievement: ")
    date_achieved = datetime.now().date()
    
    try:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO MemberAchievements (user_id, achievement_description, date_achieved) VALUES (%s, %s, %s)",
                       (user_id, achievement_description, date_achieved))
        connection.commit()
        print("Achievement added successfully!")
    except psycopg2.Error as error:
        connection.rollback()
        print("Error adding achievement:", error)


# Function to display member's achievements
def display_member_achievements(connection, user_id):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT achievement_description, date_achieved FROM MemberAchievements WHERE user_id = %s", (user_id,))
        achievements = cursor.fetchall()
        
        if achievements:
            print("Your Achievements:")
            for achievement in achievements:
                print("- Description:", achievement[0])
                print("  Date Achieved:", achievement[1])
                print()
        else:
            print("No achievements found.")
    except psycopg2.Error as error:
        print("Error fetching achievements:", error)


# Function to handle displaying, adding, updating achievements
def manage_achievements(connection, user_id):
    print("Achievements Menu")
    print("1. Add Achievement")
    print("2. View Achievements")
    print("3. Go back")
    
    choice = input("Enter your choice: ")
    print()
    
    if choice == "1":
        add_achievement(connection, user_id)
    elif choice == "2":
        display_member_achievements(connection, user_id)
    elif choice == "3":
        return
    else:
        print("Invalid choice. Please try again.")


def display_random_funny_fact(connection):
    try:
        cursor = connection.cursor()

        # Count the total number of funny fitness facts
        cursor.execute("SELECT COUNT(*) FROM FitnessFacts")
        total_facts = cursor.fetchone()[0]

        if total_facts == 0:
            print("No funny fitness facts available.")
            return

        # Generate a random number to select a random fact
        random_index = random.randint(1, total_facts)

        # Retrieve the random funny fitness fact
        cursor.execute("SELECT fact_text FROM FitnessFacts OFFSET %s LIMIT 1", (random_index - 1,))
        random_fact = cursor.fetchone()[0]

        print("Here's a funny fitness fact for you:")
        print(random_fact)
        print()
    except psycopg2.Error as error:
        print("Error fetching random funny fitness fact:", error)


def display_exercise_routines(connection):
    try:
        cursor = connection.cursor()

        # Fetch exercise routines from the database
        cursor.execute("SELECT name, description, difficulty_level, duration_minutes, calories_burned, muscle_groups FROM ExerciseRoutines")
        exercise_routines = cursor.fetchall()

        # Display exercise routines
        print("Exercise Routines:")
        for routine in exercise_routines:
            print("Name:", routine[0])
            print("Description:", routine[1])
            print("Difficulty Level:", routine[2])
            print("Duration (minutes):", routine[3])
            print("Calories Burned:", routine[4])
            print("Muscle Groups Targeted:", routine[5])
            print()  

    except psycopg2.Error as error:
        print("Error fetching exercise routines:", error)


def schedule_management(connection, user_id):
    print("Schedule Management")
    print("1. Schedule Personal Training Session")
    print("2. Schedule Group Fitness Class")
    print("3. View Personal Training Sessions")
    print("4. View Group Fitness Classes")
    print("5. Cancel a Session")
    print("6. Go back to Member Menu")

    choice = input("Enter your choice: ")
    print()

    if choice == "1":
        schedule_personal_training(connection, user_id)
    elif choice == "2":
        schedule_group_fitness_class(connection, user_id)
    elif choice == "3":
        view_personal_training_sessions(connection, user_id)
    elif choice == "4":
        view_group_fitness_classes(connection, user_id)
    elif choice == "5":
        delete_session(connection,user_id)
    elif choice == "6":
        print("Going back to Member Menu...")
        member_menu(connection,user_id)
    else:
        print("Invalid choice. Please try again.")
        print()
        schedule_management(connection, user_id)
        


def delete_session(connection,user_id):
    try:
        cursor = connection.cursor()
        
        # Fetch personal training sessions for the user
        cursor.execute("""
            SELECT ts.session_id, ts.session_date, ts.session_time
            FROM TrainingSessions ts
            INNER JOIN Members m ON ts.member_id = m.member_id
            INNER JOIN Users u ON m.user_id = u.user_id
            WHERE u.user_id = %s
            ORDER BY ts.session_date, ts.session_time
        """, (user_id,))
        
        personal_sessions = cursor.fetchall()

        if personal_sessions:
            print("Personal Training Sessions:")
            for session in personal_sessions:
                print(f"Session ID: {session[0]}, Date: {session[1]}, Time: {session[2]}")
        else:
            print("No personal training sessions found.")

        print()
    
        # Get the member_id associated with the user_id
        cursor.execute("SELECT member_id FROM Members WHERE user_id = %s", (user_id,))
        member_id = cursor.fetchone()[0] 

        # Fetch group fitness classes for the specific member
        cursor.execute("""
            SELECT gfs.session_id, cs.class_name, gfs.session_date, cs.day_of_week, cs.start_time, cs.end_time
            FROM ClassSchedule cs
            JOIN GroupFitnessSessions gfs ON cs.schedule_id = gfs.class_id
            WHERE gfs.member_id = %s
        """, (member_id,))
        group_sessions = cursor.fetchall()

        if group_sessions:
            print("Group Fitness Sessions:")
            for session in group_sessions:
                print(f"Session ID: {session[0]}, Class: {session[1]}, Date: {session[2]}, Day: {session[3]}, Time: {session[4]} - {session[5]}")
        else:
            print("No group fitness sessions found.")
            schedule_management(connection, user_id)

        
        print()
        
        session_id = input("Enter the ID of the session to delete OR 'back' to back to the Schedule Management menu): ")
        if session_id.lower() == 'back':
            print()
            schedule_management(connection,user_id)
            
        session_type = input("Enter the type of session to delete (personal/group: ")
        
        
        if session_type.lower() == 'personal':
            cursor.execute("DELETE FROM TrainingSessions WHERE session_id = %s", (session_id,))
        elif session_type.lower() == 'group':
            cursor.execute("DELETE FROM GroupFitnessSessions WHERE session_id = %s", (session_id,))
        else:
            print("Invalid session type. Please enter 'personal' or 'group'.")
            print()
            delete_session(connection,user_id)

        if cursor.rowcount > 0:
            print("Session deleted successfully!")
        else:
            print("Session not found.")
            print("Going back to member menu....")
            member_menu(connection)

        connection.commit()

    except psycopg2.Error as error:
        connection.rollback()
        print("Error deleting session")
        member_menu(connection)
        


def view_personal_training_sessions(connection, user_id):
    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT ts.session_id, ts.session_date, ts.session_time
            FROM TrainingSessions ts
            INNER JOIN Members m ON ts.member_id = m.member_id
            INNER JOIN Users u ON m.user_id = u.user_id
            WHERE u.user_id = %s
            ORDER BY ts.session_date, ts.session_time
        """, (user_id,))
        personal_sessions = cursor.fetchall()

        if personal_sessions:
            print("Personal Training Sessions:")
            for session in personal_sessions:
                print(f"Session ID: {session[0]}, Date: {session[1]}, Time: {session[2]}")
        else:
            print("No personal training sessions found.")
            print()
            schedule_management(connection, user_id)

    except psycopg2.Error as e:
        print("Error viewing personal training sessions")
        schedule_management(connection, user_id)
        

def view_group_fitness_classes(connection, user_id):
    try:
        cursor = connection.cursor()

        # Get the member_id associated with the user_id
        cursor.execute("SELECT member_id FROM Members WHERE user_id = %s", (user_id,))
        member_id = cursor.fetchone()[0]  

        # Fetch group fitness classes for the specific member
        cursor.execute("""
            SELECT gfs.session_id, cs.class_name, gfs.session_date, cs.day_of_week, cs.start_time, cs.end_time
            FROM ClassSchedule cs
            JOIN GroupFitnessSessions gfs ON cs.schedule_id = gfs.class_id
            WHERE gfs.member_id = %s
        """, (member_id,))
        group_sessions = cursor.fetchall()

        if group_sessions:
            print("Group Fitness Sessions:")
            for session in group_sessions:
                print(f"Session ID: {session[0]}, Class: {session[1]}, Date: {session[2]}, Day: {session[3]}, Time: {session[4]} - {session[5]}")
        else:
            print("No group fitness sessions found.")
            schedule_management(connection, user_id)

    except psycopg2.Error as error:
        print("Error viewing group fitness classes:", error)
        schedule_management(connection, user_id)


def schedule_personal_training(connection, user_id):
    try:
        cursor = connection.cursor()

        # Prompt member for session details
        day_of_week = input("Enter the day of the week (e.g., Monday): ")
        start_time = input("Enter the start time (HH:MM): ")

        # Fetch available trainers for the specified day and time
        cursor.execute("""
            SELECT trainer_id, full_name 
            FROM Trainers 
            WHERE trainer_id NOT IN (
                SELECT trainer_id 
                FROM TrainerSchedule 
                WHERE day_of_week = %s 
                    AND start_time <= %s 
                    AND end_time >= %s
            )
        """, (day_of_week, start_time, start_time))
        
        available_trainers = cursor.fetchall()

        if available_trainers:
            # Display available trainers to the member
            print("Available Trainers:")
            for trainer in available_trainers:
                print(f"{trainer[0]}. {trainer[1]}")

            # Prompt member to select a trainer
            trainer_id = input("Enter the ID of the selected trainer: ")

            # Prompt member to enter their full name
            member_name = input("Enter your full name: ")

            # Fetch the member ID based on the entered name
            cursor.execute("SELECT member_id FROM Members WHERE full_name = %s", (member_name,))
            member_row = cursor.fetchone()

            if member_row:
                member_id = member_row[0]
                # Insert session into database
                session_date = input("Enter the date of the session (YYYY-MM-DD): ")
                cursor.execute("""
                    INSERT INTO TrainingSessions (trainer_id, member_id, session_date, session_time) 
                    VALUES (%s, %s, %s, %s)
                """, (trainer_id, member_id, session_date, start_time))
                connection.commit()
                print("Personal training session scheduled successfully!")
            else:
                print("Member not found.")

        else:
            print("No available trainers at the specified date and time.")
            schedule_management(connection, user_id)

    except psycopg2.Error as error:
        connection.rollback()
        print("Error scheduling personal training session")
        schedule_management(connection, user_id)


def schedule_group_fitness_class(connection, user_id):
    try:
        cursor = connection.cursor()

        # Prompt member for the day to book a class
        day_of_week = input("Enter the day of the week you want to book a class (e.g., Monday): ")

        # Fetch available classes for the specified day
        cursor.execute("""
            SELECT schedule_id, class_name, start_time 
            FROM ClassSchedule 
            WHERE LOWER(day_of_week) = LOWER(%s)
        """, (day_of_week,))

        
        available_classes = cursor.fetchall()

        if available_classes:
            # Display available classes to the member
            print("Available Classes:")
            for class_info in available_classes:
                print(f"{class_info[0]}. {class_info[1]} - {class_info[2]}")

            # Prompt member to select a class
            class_id = input("Enter the ID of the selected class: ")

            # Prompt member to enter their full name
            member_name = input("Enter your full name: ")

            # Fetch the member ID based on the entered name
            cursor.execute("SELECT member_id FROM Members WHERE full_name = %s", (member_name,))
            member_row = cursor.fetchone()

            if member_row:
                member_id = member_row[0]
                # Insert class booking into database
                cursor.execute("""
                    INSERT INTO GroupFitnessSessions (class_id, member_id, session_date, session_time) 
                    SELECT schedule_id, %s, current_date, start_time 
                    FROM ClassSchedule 
                    WHERE schedule_id = %s
                """, (member_id, class_id))
                connection.commit()
                print("Class booked successfully!")
            else:
                print("Member not found.")

        else:
            print("No available classes on the specified day.")
            schedule_management(connection, user_id)

    except psycopg2.Error as error:
        connection.rollback()
        print("Error scheduling group fitness class")
        schedule_management(connection, user_id)


def update_personal_info(connection, user_id):
    while True:
        print("Updating Personal Information:")
        print("1. Full Name")
        print("2. Email")
        print("3. Phone Number")
        print("4. Address")
        print("5. Go back to Member Menu")

        choice = input("Enter your choice: ")

        if choice == "1":
            new_full_name = input("Enter your new full name: ")
            update_user_info(connection, user_id, "full_name", new_full_name)
        elif choice == "2":
            new_email = input("Enter your new email: ")
            update_user_info(connection, user_id, "email", new_email)
        elif choice == "3":
            new_phone_number = input("Enter your new phone number: ")
            update_user_info(connection, user_id, "phone_number", new_phone_number)
        elif choice == "4":
            new_address = input("Enter your new address: ")
            update_user_info(connection, user_id, "address", new_address)
        elif choice == "5":
            print("Going back to Member Menu...")
            member_menu(connection, user_id)
        else:
            print("Invalid choice. Please try again.")
        print() 


def update_user_info(connection, user_id, field, new_value):
    try:
        cursor = connection.cursor()
        cursor.execute(f"UPDATE Members SET {field} = %s WHERE user_id = %s", (new_value, user_id))
        connection.commit()
        print("Personal information updated successfully!")
    except psycopg2.Error as error:
        connection.rollback()
        print("Error updating personal information")
        update_personal_info(connection, user_id)


def update_fitness_goals(connection, user_id):
    try:
        print("Select your new fitness goal:")
        print("1. Lose Weight")
        print("2. Build Muscle")
        print("3. Improve Endurance")
        print("4. Maintain Current Fitness Level")

        choice = input("Enter your choice: ")

        fitness_goals = {
            "1": "Lose Weight",
            "2": "Build Muscle",
            "3": "Improve Endurance",
            "4": "Maintain Current Fitness Level"
        }

        if choice in fitness_goals:
            new_fitness_goal = fitness_goals[choice]

            cursor = connection.cursor()
            cursor.execute("UPDATE Members SET fitness_goal = %s WHERE user_id = %s", (new_fitness_goal, user_id))
            connection.commit()

            print("Fitness goal updated successfully!")
            print("Going back to member menu!")
            member_menu(connection,user_id)
        else:
            print("Invalid choice. Please select a valid option.")
            update_fitness_goals(connection, user_id)
    except psycopg2.Error as error:
        connection.rollback()
        print("Error updating fitness goal")
        update_fitness_goals(connection, user_id)
       
       
def update_health_metrics(connection, user_id):
    print("Updating Health Metrics:")
    print("1. Update Weight (in pounds)")
    print("2. Update Height (in feet)")
    print("3. Go back to Member Menu")

    choice = input("Enter your choice: ")

    if choice == "1":
        new_weight_pounds = float(input("Enter your new weight (in pounds): "))
        update_user_info(connection, user_id, "weight", new_weight_pounds)
        member_menu(connection, user_id)
    elif choice == "2":
        new_height_feet = float(input("Enter your new height (in feet): "))
        update_user_info(connection, user_id, "height", new_height_feet)
        member_menu(connection, user_id)
    elif choice == "3":
        print("Going back to Member Menu...")
        member_menu(connection, user_id)
    else:
        print("Invalid choice. Please try again.")
        print()
        update_health_metrics(connection, user_id)



#TRAINER FUNCTIONS: 

def tschedule_management(connection, user_id):
    trainer_id = find_trainer_id(connection, user_id)

    print("Schedule Management")

    # Prompt for the day to update
    while True:
        selected_day = input("Enter the day you want to update (e.g., Monday) OR 'back' to go back: ")
        if selected_day.capitalize() in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]:
            break
        elif selected_day.lower() == "back":
            trainer_menu(connection, user_id)
        else:
            print("Invalid day. Please enter a valid day.")


    print(f"Please enter your availability for {selected_day} (e.g., 08:00-12:00):")

    while True:
        availability = input("Enter your availability: ")
        if validate_time_format(availability):
            start_time, end_time = availability.split("-")
            update_trainer_schedule(connection, trainer_id, selected_day, start_time, end_time)
            break  
        else:
            print("Invalid time format. Please try again.")



def update_trainer_schedule(connection, trainer_id, day_of_week, start_time, end_time):
    try:
        cursor = connection.cursor()
        
        # Check if there's an existing schedule entry for the same day
        cursor.execute("SELECT * FROM TrainerSchedule WHERE trainer_id = %s AND day_of_week = %s", (trainer_id, day_of_week))
        existing_schedule = cursor.fetchone()

        if existing_schedule:
            # If an existing schedule entry exists, delete it
            cursor.execute("DELETE FROM TrainerSchedule WHERE trainer_id = %s AND day_of_week = %s", (trainer_id, day_of_week))

        # Insert the new time slot
        cursor.execute("INSERT INTO TrainerSchedule (trainer_id, day_of_week, start_time, end_time) VALUES (%s, %s, %s, %s)",
                       (trainer_id, day_of_week, start_time, end_time))
        connection.commit()
        print("Schedule updated successfully!")
    except psycopg2.Error as error:
        connection.rollback()
        print("Error updating schedule")
        print()
        trainer_menu(connection)


def member_profile_viewing(connection):
    print("Member Profile Viewing")
    print()

    # Prompt the trainer to enter the member's name
    member_name = input("Enter the member's name: ")
    print()

    try:
        cursor = connection.cursor()

        # Execute SQL query to fetch member information by name
        cursor.execute("SELECT full_name, email, phone_number, address, fitness_goal FROM Members WHERE full_name ILIKE %s", (f'%{member_name}%',))
        members = cursor.fetchall()


        if members:
            print("Found member(s):")
            for member in members:
                print("Full Name:", member[0])
                print("Email:", member[1])
                print("Phone Number:", member[2])
                print("Address:", member[3])
                print("Fitness Goal:", member[4])
                print() 
        else:
            print("No member found with that name.")

    except psycopg2.Error as error:
        print("Error fetching member information:", error)



#ADMIN FUNCTIONS: 

def room_booking_management(connection):
    while True:
        print("Room Booking Management")
        print("1. View available rooms")
        print("2. Book a room")
        print("3. View existing bookings")
        print("4. Cancel a booking")
        print("5. Return to Admin Menu")

        choice = input("Enter your choice: ")
        print()

        if choice == "1":
            day = input("Enter the date (YYYY-MM-DD): ")
            time = input("Enter the time (HH:MM): ")
            view_available_rooms(connection,day,time)
        elif choice == "2":
            book_room(connection)
        elif choice == "3":
            view_existing_bookings(connection)
        elif choice == "4":
            cancel_booking(connection)
        elif choice == "5":
            print("Returning to Admin Menu...")
            print()
            admin_menu(connection)
        else:
            print("Invalid choice. Please try again.")
            

def view_available_rooms(connection, day, time):
    try:
        cursor = connection.cursor()
        # Convert the day and time
        datetime_str = f"{day} {time}"
        datetime_obj = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")

        cursor.execute("SELECT room_id, room_name FROM Room")
        available_rooms = cursor.fetchall()
        print()
        print("Available Rooms:")
        for room in available_rooms:
            room_id, room_name = room
            # Check if the room is available at the specified day and time
            cursor.execute("SELECT COUNT(*) FROM Booking WHERE room_id = %s AND %s BETWEEN start_time AND end_time", (room_id, datetime_obj))
            count = cursor.fetchone()[0]
            if count == 0:
                print(f"{room_id}. {room_name} (Available)")
            else:
                print(f"{room_id}. {room_name} (Booked)")
    except psycopg2.Error as e:
        print("Error fetching available rooms")
        room_booking_management(connection)


def book_room(connection):
    try:
        cursor = connection.cursor()

        # Prompt admin for booking details
        while True:
            start_time = input("Enter booking start time (YYYY-MM-DD HH:MM): ")
            if not validate_time_format_book(start_time):
                print("Invalid time format. Please enter in the format YYYY-MM-DD HH:MM.")
                continue
            break

        while True:
            end_time = input("Enter booking end time (YYYY-MM-DD HH:MM): ")
            if not validate_time_format_book(end_time):
                print("Invalid time format. Please enter in the format YYYY-MM-DD HH:MM.")
                continue
            break

        purpose = input("Enter booking purpose: ")

        # Retrieve available rooms
        cursor.execute("""
            SELECT room_id, room_name
            FROM Room
            WHERE room_id NOT IN (
                SELECT room_id
                FROM Booking
                WHERE (start_time <= %s AND end_time >= %s)
                OR (start_time <= %s AND end_time >= %s)
                OR (start_time >= %s AND end_time <= %s)
            )
        """, (start_time, start_time, end_time, end_time, start_time, end_time))
        available_rooms = cursor.fetchall()

        if not available_rooms:
            print("No available rooms for the specified time range.")
            return

        # Display available rooms
        print("Available rooms:")
        for room_id, room_name in available_rooms:
            print(f"Room ID: {room_id}, Room Name: {room_name}")

        # Prompt admin to select a room
        room_id = input("Enter room ID to book: ")

        # Insert booking details into Booking table
        cursor.execute("INSERT INTO Booking (room_id, start_time, end_time, purpose) VALUES (%s, %s, %s, %s)", (room_id, start_time, end_time, purpose))
        connection.commit()
        print("Room booked successfully!")

    except psycopg2.Error as e:
        print("Error booking room")
        room_booking_management(connection) 



def view_existing_bookings(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Booking")
        existing_bookings = cursor.fetchall()
        print("Existing Bookings:")
        for booking in existing_bookings:
            booking_id, room_id, start_time, end_time, purpose, booked_by, created_at = booking
            print(f"Booking ID: {booking_id}")
            print(f"Room ID: {room_id}")
            print(f"Start Time: {start_time}")
            print(f"End Time: {end_time}")
            print(f"Purpose: {purpose}")
            print()
    except psycopg2.Error as e:
        print("Error fetching existing bookings")
        room_booking_management(connection)


def cancel_booking(connection):
    try:
        cursor = connection.cursor()
        view_existing_bookings(connection)

        booking_id = input("Enter booking ID to cancel: ")

        # Check if the booking ID exists
        cursor.execute("SELECT booking_id FROM Booking WHERE booking_id = %s", (booking_id,))
        booking = cursor.fetchone()

        if not booking:
            print("Booking ID not found.")
            return
        
        # Delete the booking
        cursor.execute("DELETE FROM Booking WHERE booking_id = %s", (booking_id,))
        connection.commit()
        print("Booking canceled successfully!")

    except psycopg2.Error as e:
        print("Error canceling booking")
        room_booking_management(connection)


def equipment_maintenance_monitoring(connection):
    try:
        cursor = connection.cursor()

        while True:
            # Fetch the list of equipment
            cursor.execute("SELECT equipment_id, equipment_name FROM Equipment")
            equipment_list = cursor.fetchall()

            # Display the list of equipment to the admin
            print("Equipment Maintenance Monitoring")
            print()
            print("List of Equipment:")
            print()
            for equipment in equipment_list:
                print(f"{equipment[0]}. {equipment[1]}")
                print()

            # Prompt the admin to select an equipment for maintenance monitoring
            equipment_id = input("Enter the ID of the equipment for maintenance monitoring (or type 'back' to return to the admin menu): ")
            
            if equipment_id.lower() == 'back':
                print("Returning to admin menu...")
                print()
                admin_menu(connection)
                break
            
            equipment_id = int(equipment_id)

            # Fetch maintenance history for the selected equipment
            cursor.execute("SELECT maintenance_id, last_maintenance_date, maintenance_notes FROM EquipmentMaintenance WHERE equipment_id = %s", (equipment_id,))
            maintenance_history = cursor.fetchall()

            if maintenance_history:
                print("Maintenance History for Selected Equipment:")
                for maintenance_record in maintenance_history:
                    print("Maintenance ID:", maintenance_record[0])
                    print("Last Maintenance Date:", maintenance_record[1])
                    print("Maintenance Notes:", maintenance_record[2])
                    print()
            else:
                print("No maintenance history found for the selected equipment.")

            # Prompt the admin to update maintenance details
            new_last_maintenance_date = input("Enter the new last maintenance date (YYYY-MM-DD): ")
            new_maintenance_notes = input("Enter maintenance notes: ")

            # Calculate the next maintenance date (6 months later)
            last_maintenance_date = datetime.strptime(new_last_maintenance_date, "%Y-%m-%d")
            next_maintenance_date = last_maintenance_date + timedelta(days=6*30)

            # Insert or update the EquipmentMaintenance table with the new maintenance details
            cursor.execute("INSERT INTO EquipmentMaintenance (equipment_id, last_maintenance_date, next_maintenance_date, maintenance_notes) VALUES (%s, %s, %s, %s) ON CONFLICT (maintenance_id) DO UPDATE SET last_maintenance_date = EXCLUDED.last_maintenance_date, next_maintenance_date = EXCLUDED.next_maintenance_date, maintenance_notes = EXCLUDED.maintenance_notes",
                (equipment_id, new_last_maintenance_date, next_maintenance_date, new_maintenance_notes))

            connection.commit()
            print("Maintenance details updated successfully!")
            print()
            admin_menu(connection)
            break 

    except psycopg2.Error as e:
        print("Error in equipment maintenance monitoring")
        equipment_maintenance_monitoring(connection)
        

def class_schedule_updating(connection):
    print("Class Schedule Updating")
    print("1. Add Class")
    print("2. Delete Class")
    print("3. Update Class")
    print("4. Return to Admin Menu")

    choice = input("Enter your choice: ")
    print()

    if choice == "1":
        add_class(connection)
    elif choice == "2":
        delete_class(connection)
    elif choice == "3":
        update_class(connection)
    elif choice == "4":
        print("Returning to Admin Menu...")
        admin_menu(connection)
        return
    else:
        print("Invalid choice. Please try again.")
        class_schedule_updating(connection)


def add_class(connection):
    try:
        cursor = connection.cursor()

        # Prompt admin for class details
        class_name = input("Enter the class name: ")
        description = input("Enter the class description: ")
        day_of_week = input("Enter the day of the week (e.g., Monday): ")
        start_time = input("Enter the start time (HH:MM): ")
        end_time = input("Enter the end time (HH:MM): ")

        # Validate time format
        if not (start_time.count(':') == 1 and end_time.count(':') == 1):
            raise ValueError("Invalid time format. Please use HH:MM format.")

        # Fetch available trainers for the specified day and time
        cursor.execute("SELECT trainer_id, full_name FROM Trainers WHERE trainer_id IN (SELECT ts.trainer_id FROM TrainerSchedule ts WHERE ts.day_of_week = %s AND ((ts.start_time <= %s AND ts.end_time > %s) OR (ts.start_time < %s AND ts.end_time >= %s)))", (day_of_week, start_time, start_time, end_time, end_time))
        available_trainers = cursor.fetchall()

        # Display available trainers to the admin
        if available_trainers:
            print("Available Trainers:")
            for trainer in available_trainers:
                print(f"{trainer[0]}. {trainer[1]}")
            # Prompt admin to select a trainer
            trainer_id = input("Enter the ID of the selected trainer: ")

            # Insert the new class into the database
            cursor.execute("INSERT INTO ClassSchedule (class_name, description, day_of_week, start_time, end_time, trainer_id) VALUES (%s, %s, %s, %s, %s, %s)", (class_name, description, day_of_week, start_time, end_time, trainer_id))
            connection.commit()

            print("Class added successfully!")
            class_schedule_updating(connection)
        else:
            print("No available trainers for the specified day and time.")
            class_schedule_updating(connection)

    except psycopg2.Error as e:
        print("Error adding class")
        class_schedule_updating(connection)



def delete_class(connection):
    try:
        cursor = connection.cursor()

        # Display existing classes to the admin
        print("Existing Classes:")
        cursor.execute("SELECT schedule_id, class_name FROM ClassSchedule")
        existing_classes = cursor.fetchall()
        for class_info in existing_classes:
            print(f"{class_info[0]}. {class_info[1]}")

        # Prompt admin to select a class to delete
        class_id = input("Enter the ID of the class to delete: ")

        # Check if the selected class exists
        cursor.execute("SELECT * FROM ClassSchedule WHERE schedule_id = %s", (class_id,))
        class_exists = cursor.fetchone()

        if class_exists:
            # Delete the class from the database
            cursor.execute("DELETE FROM ClassSchedule WHERE schedule_id = %s", (class_id,))
            connection.commit()
            print("Class deleted successfully!")
            print()
            class_schedule_updating(connection)
            
        else:
            print("Class not found.")

    except psycopg2.Error as error:
        connection.rollback() 
        print("Error deleting class")
        class_schedule_updating(connection)
        

def update_class(connection):
    try:
        cursor = connection.cursor()

        # Display existing classes to the admin
        print("Existing Classes:")
        cursor.execute("SELECT schedule_id, class_name FROM ClassSchedule")
        existing_classes = cursor.fetchall()
        for class_info in existing_classes:
            print(f"{class_info[0]}. {class_info[1]}")

        # Prompt admin to select a class to update
        class_id = input("Enter the ID of the class to update: ")

        # Fetch details of the selected class
        cursor.execute("SELECT class_name, description, day_of_week, start_time, end_time, trainer_id FROM ClassSchedule WHERE schedule_id = %s", (class_id,))
        class_details = cursor.fetchone()

        if class_details:
            # Ask admin what they want to update
            print("What do you want to update?")
            print("1. Class Name")
            print("2. Class Description")
            print("3. Day of the Week")
            print("4. Start Time")
            print("5. End Time")
            print("6. Trainer ID")
            choice = input("Enter your choice (1-6): ")

            # Prompt admin for the updated value based on their choice
            if choice == "1":
                new_value = input("Enter the updated class name: ")
                # Update the class name in the database
                cursor.execute("UPDATE ClassSchedule SET class_name = %s WHERE schedule_id = %s", (new_value, class_id))
            elif choice == "2":
                new_value = input("Enter the updated class description: ")
                # Update the class description in the database
                cursor.execute("UPDATE ClassSchedule SET description = %s WHERE schedule_id = %s", (new_value, class_id))
            elif choice == "3":
                new_value = input("Enter the updated day of the week: ")
                # Update the day of the week in the database
                cursor.execute("UPDATE ClassSchedule SET day_of_week = %s WHERE schedule_id = %s", (new_value, class_id))
            elif choice == "4":
                new_value = input("Enter the updated start time (HH:MM): ")
                # Update the start time in the database
                cursor.execute("UPDATE ClassSchedule SET start_time = %s WHERE schedule_id = %s", (new_value, class_id))
            elif choice == "5":
                new_value = input("Enter the updated end time (HH:MM): ")
                # Update the end time in the database
                cursor.execute("UPDATE ClassSchedule SET end_time = %s WHERE schedule_id = %s", (new_value, class_id))
            elif choice == "6":
                new_value = input("Enter the updated trainer ID: ")
                # Update the trainer ID in the database
                cursor.execute("UPDATE ClassSchedule SET trainer_id = %s WHERE schedule_id = %s", (new_value, class_id))
            else:
                print("Invalid choice.")
                return

            connection.commit() 
            print("Class updated successfully!")

            # Ask if admin wants to update another attribute
            update_another = input("Do you want to update another class? (yes/no): ").lower()
            if update_another == "yes":
                update_class(connection)
            if update_another == "no":
                admin_menu(connection)

        else:
            print("Class not found.")

    except psycopg2.Error as e:
        connection.rollback()  
        print("Error updating class")
        class_schedule_updating(connection)


def charge_cards(connection):
    try:
        cursor = connection.cursor()

        # Retrieve users with outstanding payments
        cursor.execute("SELECT user_id FROM Subscriptions WHERE payment_status = false")
        users = cursor.fetchall()

        # Display users who owe money
        if users:
            print("Users with outstanding payments:")
            for user in users:
                print(user[0])  
        else:
            print("No members have outstanding payments.")
            print()
            admin_menu(connection)

        # Prompt the admin to confirm the charging process
        confirmation = input("Do you want to proceed with charging these users? (yes/no): ").lower()
        if confirmation == "yes":
            # Simulate charging the cards
            for user in users:
                user_id = user[0]
                # Update the payment_date to mark that the user has been charged
                cursor.execute("UPDATE Subscriptions SET payment_date = %s, payment_status = true WHERE user_id = %s", (datetime.now(), user_id))

            connection.commit()
            print("Charging process completed successfully!")
            admin_menu(connection)
        else:
            print("Charging process aborted.")
            admin_menu(connection)

    except psycopg2.Error as e:
        connection.rollback()
        print("Error charging cards")
        admin_menu(connection)


#EXTRA/HELPERS: 

def find_trainer_id(connection, user_id):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT trainer_id FROM Trainers WHERE user_id = %s", (user_id,))
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            print("Trainer ID not found.")
            return None
    except psycopg2.Error as e:
        print("Error retrieving trainer ID")
        return None


def validate_time_format(time_string):
    parts = time_string.split("-")
    if len(parts) == 2:
        start_time, end_time = parts
        try:
            datetime.strptime(start_time, "%H:%M")
            datetime.strptime(end_time, "%H:%M")
            return True
        except ValueError:
            return False
    return False


def validate_time_format_book(time_str):
    time_pattern = re.compile(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}$')
    return bool(time_pattern.match(time_str))


def main():
    # Create a connection to the PostgreSQL database
    connection = create_connection()

    # If connection successful
    if connection:
        try:
            user_id, user_role = start_menu(connection)
            if user_id is not None and user_role is not None:
                # Display menu based on user's role
                if user_role == "admin":
                    admin_menu(connection)
                elif user_role == "member":
                    member_menu(connection, user_id)  
                elif user_role == "trainer":
                    trainer_menu(connection, user_id)
        except TypeError:
            main() 

if __name__ == "__main__":
    main()
