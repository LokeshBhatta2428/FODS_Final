import os
import matplotlib.pyplot as plt
from getpass import getpass

class User:
    def __init__(self, username, password, role, user_id, name, email):
        self.username = username
        self.password = password
        self.role = role
        self.user_id = user_id
        self.name = name
        self.email = email

    def save_to_files(self):
        # Save to users.txt
        with open('users.txt', 'a') as f:
            f.write(f"{self.user_id},{self.username},{self.name},{self.email},{self.role}\n")
        
        # Save to passwords.txt
        with open('passwords.txt', 'a') as f:
            f.write(f"{self.username},{self.password}\n")
        
        # Initialize empty records in grades.txt and eca.txt if role is student
        if self.role == 'student':
            # Check if record already exists in grades.txt
            exists = False
            if os.path.exists('grades.txt'):
                with open('grades.txt', 'r') as f:
                    for line in f:
                        if line.startswith(f"{self.user_id},"):
                            exists = True
                            break
            
            if not exists:
                with open('grades.txt', 'a') as f:
                    f.write(f"{self.user_id},,,,,,\n")
                
            # Check if record already exists in eca.txt
            exists = False
            if os.path.exists('eca.txt'):
                with open('eca.txt', 'r') as f:
                    for line in f:
                        if line.startswith(f"{self.user_id},"):
                            exists = True
                            break
            
            if not exists:
                with open('eca.txt', 'a') as f:
                    f.write(f"{self.user_id},,\n")

class Student(User):
    def view_profile(self):
        print("\n=== Student Profile ===")
        print(f"ID: {self.user_id}")
        print(f"Name: {self.name}")
        print(f"Email: {self.email}")
        
        # Get grades
        if os.path.exists('grades.txt'):
            with open('grades.txt', 'r') as f:
                for line in f:
                    data = line.strip().split(',')
                    if data[0] == self.user_id:
                        print("\nGrades:")
                        print(f"Math: {data[1] if len(data) > 1 and data[1] else 'Not graded'}")
                        print(f"Science: {data[2] if len(data) > 2 and data[2] else 'Not graded'}")
                        print(f"English: {data[3] if len(data) > 3 and data[3] else 'Not graded'}")
                        print(f"History: {data[4] if len(data) > 4 and data[4] else 'Not graded'}")
                        print(f"Art: {data[5] if len(data) > 5 and data[5] else 'Not graded'}")
                        break
        
        # Get ECA
        if os.path.exists('eca.txt'):
            with open('eca.txt', 'r') as f:
                for line in f:
                    data = line.strip().split(',')
                    if data[0] == self.user_id:
                        eca = data[1] if len(data) > 1 and data[1] else "None"
                        print(f"\nExtracurricular Activities: {eca}")
                        break
    
    def update_profile(self):
        print("\nUpdate Profile Information")
        new_name = input(f"Name (current: {self.name}): ") or self.name
        new_email = input(f"Email (current: {self.email}): ") or self.email
        
        # Update in users.txt
        updated_users = []
        with open('users.txt', 'r') as f:
            for line in f:
                data = line.strip().split(',')
                if data[0] == self.user_id:
                    data[2] = new_name
                    data[3] = new_email
                    updated_users.append(','.join(data))
                else:
                    updated_users.append(line.strip())
        
        with open('users.txt', 'w') as f:
            f.write('\n'.join(updated_users) + '\n')
        
        self.name = new_name
        self.email = new_email
        print("Profile updated successfully!")

    def view_grades_chart(self):
        subjects = ['Math', 'Science', 'English', 'History', 'Art']
        grades = [0, 0, 0, 0, 0]  # Default to 0
        
        if os.path.exists('grades.txt'):
            with open('grades.txt', 'r') as f:
                for line in f:
                    data = line.strip().split(',')
                    if data[0] == self.user_id:
                        # Handle possible index errors by checking length
                        for i in range(1, min(len(data), 6)):
                            if data[i].strip():  # If grade exists and is not empty
                                try:
                                    grades[i-1] = int(data[i])
                                except ValueError:
                                    grades[i-1] = 0  # Set to 0 if conversion fails
                        break
        
        plt.figure(figsize=(10, 6))
        plt.bar(subjects, grades)
        plt.title('My Grades')
        plt.ylabel('Score')
        plt.ylim(0, 100)
        plt.show()

class Admin(User):
    def add_user(self):
        print("\nAdd New User")
        user_id = input("User ID: ")
        username = input("Username: ")
        password = input("Password: ")
        name = input("Full Name: ")
        email = input("Email: ")
        role = input("Role (admin/student): ").lower()
        
        while role not in ['admin', 'student']:
            print("Invalid role. Must be 'admin' or 'student'.")
            role = input("Role (admin/student): ").lower()
        
        new_user = User(username, password, role, user_id, name, email)
        new_user.save_to_files()
        print(f"{role.capitalize()} user added successfully!")

    def modify_student_record(self):
        print("\nModify Student Record")
        user_id = input("Enter student ID: ")
        
        # Check if user exists
        user_found = False
        if os.path.exists('users.txt'):
            with open('users.txt', 'r') as f:
                for line in f:
                    data = line.strip().split(',')
                    if len(data) >= 5 and data[0] == user_id and data[4] == 'student':
                        user_found = True
                        break
        
        if not user_found:
            print("Student not found!")
            return
        
        print("\nWhat would you like to modify?")
        print("1. Personal Information")
        print("2. Grades")
        print("3. ECA")
        choice = input("Enter choice (1-3): ")
        
        if choice == '1':
            self._modify_personal_info(user_id)
        elif choice == '2':
            self._modify_grades(user_id)
        elif choice == '3':
            self._modify_eca(user_id)
        else:
            print("Invalid choice!")

    def _modify_personal_info(self, user_id):
        updated_users = []
        found = False
        
        with open('users.txt', 'r') as f:
            for line in f:
                data = line.strip().split(',')
                if len(data) >= 5 and data[0] == user_id:
                    found = True
                    print(f"\nCurrent Information for {data[2]}:")
                    print(f"1. Username: {data[1]}")
                    print(f"2. Name: {data[2]}")
                    print(f"3. Email: {data[3]}")
                    
                    field = input("\nWhich field to update? (1-3): ")
                    if field == '1':
                        new_username = input("New username: ")
                        # Also update username in passwords.txt
                        self._update_username_in_passwords(data[1], new_username)
                        data[1] = new_username
                    elif field == '2':
                        data[2] = input("New name: ")
                    elif field == '3':
                        data[3] = input("New email: ")
                    else:
                        print("Invalid field!")
                        return
                    
                    updated_users.append(','.join(data))
                else:
                    updated_users.append(line.strip())
        
        if not found:
            print("Student not found!")
            return
            
        with open('users.txt', 'w') as f:
            
            f.write('\n'.join(updated_users) + '\n')
        
        print("Personal information updated successfully!")

    def _update_username_in_passwords(self, old_username, new_username):
        updated_passwords = []
        password = None
        
        with open('passwords.txt', 'r') as f:
            for line in f:
                data = line.strip().split(',')
                if len(data) >= 2 and data[0] == old_username:
                    password = data[1]
                    updated_passwords.append(f"{new_username},{password}")
                else:
                    updated_passwords.append(line.strip())
        
        with open('passwords.txt', 'w') as f:
            f.write('\n'.join(updated_passwords) + '\n')

    def _modify_grades(self, user_id):
        updated_grades = []
        found = False
        
        # Ensure grades.txt exists
        if not os.path.exists('grades.txt'):
            with open('grades.txt', 'w') as f:
                pass
                
        # Check if student has a record in grades.txt
        student_has_record = False
        with open('grades.txt', 'r') as f:
            for line in f:
                if line.startswith(f"{user_id},"):
                    student_has_record = True
                    break
        
        # If student doesn't have a record, create one
        if not student_has_record:
            with open('grades.txt', 'a') as f:
                f.write(f"{user_id},,,,,,\n")
        
        with open('grades.txt', 'r') as f:
            for line in f:
                data = line.strip().split(',')
                if data[0] == user_id:
                    found = True
                    # Make sure we have enough elements for all subjects
                    while len(data) < 6:
                        data.append("")
                        
                    print("\nCurrent Grades:")
                    subjects = ['Math', 'Science', 'English', 'History', 'Art']
                    for i in range(5):
                        current = data[i+1] if i+1 < len(data) and data[i+1] else "Not graded"
                        print(f"{i+1}. {subjects[i]}: {current}")
                    
                    subject = input("\nWhich subject to update? (1-5): ")
                    if subject in ['1', '2', '3', '4', '5']:
                        subj_idx = int(subject)
                        new_grade = input(f"New grade for {subjects[subj_idx-1]} (0-100): ")
                        try:
                            grade_value = int(new_grade)
                            if 0 <= grade_value <= 100:
                                data[subj_idx] = new_grade
                            else:
                                print("Grade must be between 0 and 100!")
                                return
                        except ValueError:
                            print("Please enter a valid number!")
                            return
                            
                        updated_grades.append(','.join(data))
                    else:
                        print("Invalid subject!")
                        return
                else:
                    updated_grades.append(line.strip())
        
        if not found:
            print("Student not found in grades records!")
            return
        
        with open('grades.txt', 'w') as f:
            f.write('\n'.join(updated_grades) + '\n')
        
        print("Grades updated successfully!")

    def _modify_eca(self, user_id):
        updated_ecas = []
        found = False
        
        # Ensure eca.txt exists
        if not os.path.exists('eca.txt'):
            with open('eca.txt', 'w') as f:
                pass
                
        # Check if student has a record in eca.txt
        student_has_record = False
        with open('eca.txt', 'r') as f:
            for line in f:
                if line.startswith(f"{user_id},"):
                    student_has_record = True
                    break
        
        # If student doesn't have a record, create one
        if not student_has_record:
            with open('eca.txt', 'a') as f:
                f.write(f"{user_id},,\n")
        
        with open('eca.txt', 'r') as f:
            for line in f:
                data = line.strip().split(',')
                if data[0] == user_id:
                    found = True
                    # Make sure we have enough elements
                    while len(data) < 2:
                        data.append("")
                        
                    current_eca = data[1] if len(data) > 1 and data[1] else "None"
                    print(f"\nCurrent ECA: {current_eca}")
                    new_eca = input("New ECA activities (comma separated): ")
                    data[1] = new_eca
                    updated_ecas.append(','.join(data))
                else:
                    updated_ecas.append(line.strip())
        
        if not found:
            print("Student not found in ECA records!")
            return
        
        with open('eca.txt', 'w') as f:
            f.write('\n'.join(updated_ecas) + '\n')
        
        print("ECA updated successfully!")

    def delete_student(self):
        user_id = input("\nEnter student ID to delete: ")
        
        # Verify student exists
        user_found = False
        username = None
        
        if os.path.exists('users.txt'):
            with open('users.txt', 'r') as f:
                for line in f:
                    data = line.strip().split(',')
                    if len(data) >= 5 and data[0] == user_id and data[4] == 'student':
                        user_found = True
                        username = data[1]
                        break
        
        if not user_found:
            print("Student not found!")
            return
        
        # Confirm deletion
        confirm = input(f"Are you sure you want to delete student {user_id}? (y/n): ").lower()
        if confirm != 'y':
            print("Deletion cancelled.")
            return
        
        # Delete from users.txt
        if os.path.exists('users.txt'):
            updated_users = []
            with open('users.txt', 'r') as f:
                for line in f:
                    data = line.strip().split(',')
                    if len(data) == 0 or data[0] != user_id:
                        updated_users.append(line.strip())
            
            with open('users.txt', 'w') as f:
                if updated_users:
                    f.write('\n'.join(updated_users) + '\n')
                else:
                    f.write("")
        
        # Delete from passwords.txt
        if os.path.exists('passwords.txt') and username:
            updated_passwords = []
            with open('passwords.txt', 'r') as f:
                for line in f:
                    data = line.strip().split(',')
                    if len(data) == 0 or data[0] != username:
                        updated_passwords.append(line.strip())
            
            with open('passwords.txt', 'w') as f:
                if updated_passwords:
                    f.write('\n'.join(updated_passwords) + '\n')
                else:
                    f.write("")
        
        # Delete from grades.txt
        if os.path.exists('grades.txt'):
            updated_grades = []
            with open('grades.txt', 'r') as f:
                for line in f:
                    data = line.strip().split(',')
                    if len(data) == 0 or data[0] != user_id:
                        updated_grades.append(line.strip())
            
            with open('grades.txt', 'w') as f:
                if updated_grades:
                    f.write('\n'.join(updated_grades) + '\n')
                else:
                    f.write("")
        
        # Delete from eca.txt
        if os.path.exists('eca.txt'):
            updated_ecas = []
            with open('eca.txt', 'r') as f:
                for line in f:
                    data = line.strip().split(',')
                    if len(data) == 0 or data[0] != user_id:
                        updated_ecas.append(line.strip())
            
            with open('eca.txt', 'w') as f:
                if updated_ecas:
                    f.write('\n'.join(updated_ecas) + '\n')
                else:
                    f.write("")
        
        print("Student deleted successfully!")

    def generate_insights(self):
        print("\n=== Data Insights ===")
        print("1. Average grades per subject")
        print("2. Most active students in ECA")
        print("3. Grade distribution visualization")
        choice = input("Enter choice (1-3): ")
        
        if choice == '1':
            self._average_grades()
        elif choice == '2':
            self._most_active_students()
        elif choice == '3':
            self._grade_distribution()
        else:
            print("Invalid choice!")

    def _average_grades(self):
        subjects = ['Math', 'Science', 'English', 'History', 'Art']
        totals = [0, 0, 0, 0, 0]
        counts = [0, 0, 0, 0, 0]
        
        if not os.path.exists('grades.txt'):
            print("No grade data available!")
            return
            
        with open('grades.txt', 'r') as f:
            for line in f:
                data = line.strip().split(',')
                if len(data) < 6:  # Skip invalid lines
                    continue
                    
                for i in range(1, 6):
                    if i < len(data) and data[i]:  # If grade exists
                        try:
                            totals[i-1] += int(data[i])
                            counts[i-1] += 1
                        except ValueError:
                            # Skip invalid grades
                            pass
        
        print("\nAverage Grades:")
        for i in range(5):
            if counts[i] > 0:
                avg = totals[i] / counts[i]
                print(f"{subjects[i]}: {avg:.2f}")
            else:
                print(f"{subjects[i]}: No data")

    def _most_active_students(self):
        eca_counts = {}
        name_map = {}
        
        # Create name mapping
        if not os.path.exists('users.txt'):
            print("No user data available!")
            return
            
        with open('users.txt', 'r') as f:
            for line in f:
                data = line.strip().split(',')
                if len(data) >= 5 and data[4] == 'student':
                    name_map[data[0]] = data[2]
        
        # Count ECA activities
        if not os.path.exists('eca.txt'):
            print("No ECA data available!")
            return
            
        with open('eca.txt', 'r') as f:
            for line in f:
                data = line.strip().split(',')
                if len(data) >= 2 and data[0] in name_map and data[1]:
                    activity_count = len(data[1].split(','))
                    eca_counts[name_map[data[0]]] = activity_count
        
        if not eca_counts:
            print("No ECA data available!")
            return
        
        sorted_students = sorted(eca_counts.items(), key=lambda x: x[1], reverse=True)
        
        print("\nMost Active Students in ECA:")
        for i, (name, count) in enumerate(sorted_students[:5], 1):
            print(f"{i}. {name}: {count} activities")

    def _grade_distribution(self):
        subjects = ['Math', 'Science', 'English', 'History', 'Art']
        grades = [[] for _ in range(5)]
        
        if not os.path.exists('grades.txt'):
            print("No grade data available!")
            return
            
        with open('grades.txt', 'r') as f:
            for line in f:
                data = line.strip().split(',')
                if len(data) < 6:  # Skip invalid lines
                    continue
                    
                for i in range(1, 6):
                    if i < len(data) and data[i]:
                        try:
                            grades[i-1].append(int(data[i]))
                        except ValueError:
                            # Skip invalid grades
                            pass
        
        # Check if we have data to plot
        has_data = False
        for subject_grades in grades:
            if subject_grades:
                has_data = True
                break
                
        if not has_data:
            print("No grade data available for visualization!")
            return
            
        plt.figure(figsize=(10, 6))
        plt.boxplot(grades, labels=subjects)
        plt.title('Grade Distribution by Subject')
        plt.ylabel('Score')
        plt.ylim(0, 100)
        plt.show()

def initialize_files():
    # Create files if they don't exist
    if not os.path.exists('users.txt'):
        with open('users.txt', 'w') as f:
            f.write("")
    
    if not os.path.exists('passwords.txt'):
        with open('passwords.txt', 'w') as f:
            f.write("admin,admin123\n")  # Default admin account
    
    if not os.path.exists('grades.txt'):
        with open('grades.txt', 'w') as f:
            f.write("")
    
    if not os.path.exists('eca.txt'):
        with open('eca.txt', 'w') as f:
            f.write("")
    
    # Add default admin if not exists in users.txt
    admin_exists = False
    with open('users.txt', 'r') as f:
        for line in f:
            if line.strip().endswith('admin'):
                admin_exists = True
                break
    
    if not admin_exists:
        with open('users.txt', 'a') as f:
            f.write("ADM001,admin,Administrator,admin@school.edu,admin\n")

def username_from_id(user_id):
    if not os.path.exists('users.txt'):
        return None
        
    with open('users.txt', 'r') as f:
        for line in f:
            data = line.strip().split(',')
            if len(data) >= 2 and data[0] == user_id:
                return data[1]
    return None

def login():
    print("\n=== Login ===")
    username = input("Username: ")
    password = getpass("Password: ")
    
    # Check if passwords file exists
    if not os.path.exists('passwords.txt'):
        print("Password file not found. System might not be initialized properly.")
        return None
    
    # Check password
    with open('passwords.txt', 'r') as f:
        for line in f:
            data = line.strip().split(',')
            if len(data) >= 2 and data[0] == username and data[1] == password:
                # Get user details
                if not os.path.exists('users.txt'):
                    print("User data file not found. System might not be initialized properly.")
                    return None
                    
                with open('users.txt', 'r') as users_file:
                    for user_line in users_file:
                        user_data = user_line.strip().split(',')
                        if len(user_data) >= 5 and user_data[1] == username:
                            if user_data[4] == 'admin':
                                return Admin(username, password, 'admin', user_data[0], user_data[2], user_data[3])
                            else:
                                return Student(username, password, 'student', user_data[0], user_data[2], user_data[3])
    
    print("Invalid username or password!")
    return None

def student_menu(student):
    while True:
        print("\n=== Student Menu ===")
        print("1. View Profile")
        print("2. Update Profile")
        print("3. View Grades Chart")
        print("4. Logout")
        
        choice = input("Enter choice (1-4): ")
        
        if choice == '1':
            student.view_profile()
        elif choice == '2':
            student.update_profile()
        elif choice == '3':
            student.view_grades_chart()
        elif choice == '4':
            print("Logging out...")
            break
        else:
            print("Invalid choice!")

def admin_menu(admin):
    while True:
        print("\n=== Admin Menu ===")
        print("1. Add New User")
        print("2. Modify Student Record")
        print("3. Delete Student")
        print("4. Generate Insights")
        print("5. Logout")
        
        choice = input("Enter choice (1-5): ")
        
        if choice == '1':
            admin.add_user()
        elif choice == '2':
            admin.modify_student_record()
        elif choice == '3':
            admin.delete_student()
        elif choice == '4':
            admin.generate_insights()
        elif choice == '5':
            print("Logging out...")
            break
        else:
            print("Invalid choice!")

def main():
    initialize_files()
    
    while True:
        print("\n=== Student Profile Management System ===")
        print("1. Login")
        print("2. Exit")
        
        choice = input("Enter choice (1-2): ")
        
        if choice == '1':
            user = login()
            if user:
                if user.role == 'admin':
                    admin_menu(user)
                else:
                    student_menu(user)
        elif choice == '2':
            print("Exiting system. Goodbye!")
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()                                                              

                                                                                              