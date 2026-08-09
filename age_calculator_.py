from datetime import date, datetime, timedelta

def calculate_age(birthday):
    today = date.today()
    if today < birthday:
        return "Invalid birthdate. Please enter a valid date."
    year_diff, month_diff, day_diff = today.year - birthday.year, today.month - birthday.month, today.day - birthday.day
    if day_diff < 0:
        month_diff -= 1
        day_diff += (today.replace(day=1) - timedelta(days=1)).day
    if month_diff < 0:
        year_diff -= 1
        month_diff += 12
    return f"Age: {year_diff} years, {month_diff} months, and {day_diff} days"

if __name__ == "__main__":
    try:
        birthdate_input = input("Enter the birthdate (DD/MM/YYYY): ")
        dateOfBirth = datetime.strptime(birthdate_input, "%d/%m/%Y").date()
        print(calculate_age(dateOfBirth))
    except ValueError:
        print("Invalid input. Please enter the date in the format DD/MM/YYYY.")