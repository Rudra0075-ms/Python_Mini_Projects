def pounds_to_kg(pounds):
    conversion_factor = 0.453592 
    kilograms = pounds * conversion_factor
    return kilograms

def main():
    pounds = float(input("Enter the weight in pounds: "))
    kilograms = pounds_to_kg(pounds)
    print(f"{pounds} pounds is equal to {kilograms:.2f} kilograms")

if __name__ == "__main__":
    main()
    