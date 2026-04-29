import json
import os

FILE_NAME = "students.json"

students = []
last_id = 1


def load_data():
    global students, last_id

    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r", encoding="utf-8") as file:
            data = json.load(file)
            students = data.get("students", [])
            last_id = data.get("last_id", 1)


def save_data():
    data = {
        "students": students,
        "last_id": last_id
    }

    with open(FILE_NAME, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def get_grade(prompt):
    while True:
        try:
            value = float(input(prompt))

            if 0 <= value <= 100:
                return value
            else:
                print("Error: Grade must be between 0 and 100.\n")

        except ValueError:
            print("Error: Please enter a valid number.\n")


def calculate_letter_grade(average):
    if average >= 90:
        return "AA"
    elif average >= 80:
        return "BA"
    elif average >= 70:
        return "BB"
    elif average >= 60:
        return "CB"
    elif average >= 50:
        return "CC"
    else:
        return "FF"


def calculate_status(average):
    return "Passed" if average >= 50 else "Failed"


def print_student(student):
    print("\n--- Student Information ---")
    print(f"ID: {student['id']}")
    print(f"Name: {student['name']} {student['surname']}")
    print(f"Midterm: {student['midterm']}")
    print(f"Final: {student['final']}")
    print(f"Average: {student['average']:.2f}")
    print(f"Letter Grade: {student['letter_grade']}")
    print(f"Status: {student['status']}")
    print("-" * 30)


def add_student():
    global last_id

    name = input("Student name: ").strip().title()
    surname = input("Student surname: ").strip().title()

    midterm = get_grade("Midterm grade: ")
    final = get_grade("Final grade: ")

    average = (midterm * 0.4) + (final * 0.6)

    student = {
        "id": last_id,
        "name": name,
        "surname": surname,
        "midterm": midterm,
        "final": final,
        "average": average,
        "letter_grade": calculate_letter_grade(average),
        "status": calculate_status(average)
    }

    students.append(student)
    last_id += 1
    save_data()

    print("Student successfully added.\n")


def list_students():
    if len(students) == 0:
        print("No students found.\n")
        return

    print("\n--- Student List ---")
    for student in students:
        print(
            f"ID: {student['id']} | "
            f"{student['name']} {student['surname']} | "
            f"Average: {student['average']:.2f} | "
            f"Grade: {student['letter_grade']} | "
            f"{student['status']}"
        )
    print()


def find_student_by_id(student_id):
    for student in students:
        if student["id"] == student_id:
            return student
    return None


def delete_student():
    if len(students) == 0:
        print("No students to delete.\n")
        return

    list_students()

    try:
        student_id = int(input("Enter student ID to delete: "))
        student = find_student_by_id(student_id)

        if student:
            students.remove(student)
            save_data()
            print("Student deleted.\n")
        else:
            print("Student not found.\n")

    except ValueError:
        print("Invalid ID.\n")


def update_student():
    if len(students) == 0:
        print("No students to update.\n")
        return

    list_students()

    try:
        student_id = int(input("Enter student ID to update: "))
        student = find_student_by_id(student_id)

        if not student:
            print("Student not found.\n")
            return

        print(f"Selected: {student['name']} {student['surname']}")

        name = input("New name: ").strip().title()
        surname = input("New surname: ").strip().title()
        midterm = get_grade("New midterm grade: ")
        final = get_grade("New final grade: ")

        average = (midterm * 0.4) + (final * 0.6)

        student["name"] = name
        student["surname"] = surname
        student["midterm"] = midterm
        student["final"] = final
        student["average"] = average
        student["letter_grade"] = calculate_letter_grade(average)
        student["status"] = calculate_status(average)

        save_data()
        print("Student updated.\n")

    except ValueError:
        print("Invalid input.\n")


def select_from_list(results):
    if len(results) == 0:
        print("No students found.\n")
        return

    print("\n--- Matching Students ---")
    for i, student in enumerate(results, start=1):
        print(f"{i}- {student['name']} {student['surname']} (ID: {student['id']})")

    try:
        choice = int(input("Select a student: "))

        if 1 <= choice <= len(results):
            print_student(results[choice - 1])
        else:
            print("Invalid selection.\n")

    except ValueError:
        print("Please enter a number.\n")


def search_student():
    if len(students) == 0:
        print("No students to search.\n")
        return

    while True:
        print("\n--- Search Menu ---")
        print("1- By ID")
        print("2- By name")
        print("3- By surname")
        print("4- By first letter")
        print("5- Back")

        choice = input("Choice: ")

        if choice == "1":
            try:
                student_id = int(input("Student ID: "))
                student = find_student_by_id(student_id)

                if student:
                    print_student(student)
                else:
                    print("Not found.\n")

            except ValueError:
                print("Invalid input.\n")

        elif choice == "2":
            name = input("Enter name: ").lower()
            results = [s for s in students if name in s["name"].lower()]
            select_from_list(results)

        elif choice == "3":
            surname = input("Enter surname: ").lower()
            results = [s for s in students if surname in s["surname"].lower()]
            select_from_list(results)

        elif choice == "4":
            letter = input("First letter: ").lower()

            if len(letter) != 1:
                print("Enter only one letter.\n")
                continue

            results = [s for s in students if s["name"].lower().startswith(letter)]
            select_from_list(results)

        elif choice == "5":
            break

        else:
            print("Invalid choice.\n")


def menu():
    while True:
        print("\n" + "=" * 35)
        print("      STUDENT SYSTEM")
        print("=" * 35)
        print("1- Add Student")
        print("2- List Students")
        print("3- Delete Student")
        print("4- Update Student")
        print("5- Search Student")
        print("6- Exit")
        print("=" * 35)

        choice = input("Choice: ")

        if choice == "1":
            add_student()
        elif choice == "2":
            list_students()
        elif choice == "3":
            delete_student()
        elif choice == "4":
            update_student()
        elif choice == "5":
            search_student()
        elif choice == "6":
            print("Exiting...")
            break
        else:
            print("Invalid choice.\n")


load_data()
menu()