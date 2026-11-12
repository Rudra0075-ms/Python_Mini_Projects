from database import initialize_database
from register_face import register_student
from attendance import run_attendance

def main():
    initialize_database()

    while True:
        print("\n===== FACE RECOGNITION ATTENDANCE =====")
        print("1. Register student from an image")
        print("2. Start attendance webcam")
        print("3. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            register_student()
        elif choice == "2":
            run_attendance()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Enter 1, 2, or 3.")

if __name__ == "__main__":
    main()
