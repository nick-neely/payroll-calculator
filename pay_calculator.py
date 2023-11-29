import json
import datetime


def calculate_payroll():
    """
    Calculates the payroll summary based on the number of hours worked and hourly wage.

    Returns:
        A tuple containing the total hours worked, gross pay, FICA tax, and net pay.
    """
    try:
        # Initialize the hours worked
        total_hours_worked = 0.0

        while True:
            # Ask the user for the number of hours worked
            hours_worked = input("Please enter the number of hours worked (or 'done' to finish): ")
            
            if hours_worked.lower() == 'done':
                break

            total_hours_worked += float(hours_worked)

        # Define the hourly wage
        hourly_wage = 20.0

        # Calculate the gross pay
        gross_pay = total_hours_worked * hourly_wage

        # Calculate the FICA tax
        fica_tax_rate = 7.65 / 100
        fica_tax = gross_pay * fica_tax_rate

        # Calculate the net pay
        net_pay = gross_pay - fica_tax

        # Print the total hours worked
        print("\nPayroll Summary")
        print("-------------------------")
        print(f"Total Hours Worked: {total_hours_worked:.2f}")

        # Print the gross pay, FICA tax, and net pay
        print(f"Gross Pay ({total_hours_worked} * ${hourly_wage}): ${gross_pay:.2f}")
        print(f"FICA Tax (${gross_pay} * {fica_tax_rate}): ${fica_tax:.2f}")
        print(f"Net Pay (${gross_pay} - ${fica_tax:.2f}): ${net_pay:.2f}")

        print("-------------------------")

    except ValueError:
        print("Invalid input. Please enter a valid number of hours.")

    return total_hours_worked, gross_pay, fica_tax, net_pay


def save_payroll(name, total_hours_worked, gross_pay, fica_tax, net_pay):
    """
    Save the payroll summary to a JSON file.

    Args:
        total_hours_worked (float): The total number of hours worked.
        gross_pay (float): The gross pay amount.
        fica_tax (float): The FICA tax amount.
        net_pay (float): The net pay amount.

    Raises:
        IOError: If there is an error saving the payroll summary to the file.
    """
    try:
        # Create a dictionary for the payroll summary
        payroll_summary = {
            "Name": name,
            "Total Hours": total_hours_worked,
            "Date": datetime.datetime.now().strftime("%Y-%m-%d"),
            "Gross Pay": round(gross_pay, 2),
            "FICA Tax": round(fica_tax, 2),
            "Net Pay": round(net_pay, 2)
        }
        
        # Specify the full path to the file
        file_path = r"payroll_summary.json"

        # Read the existing data from the file
        try:
            with open(file_path, "r") as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            data = []

        # Append the new payroll summary
        data.append(payroll_summary)

        # Write the data back to the file
        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)

        print("Payroll summary saved to payroll_summary.json")

    except IOError:
        print("Error saving payroll summary to file.")

def main():
    """
    The main function.
    """
    calculate_again = 'y'
    while calculate_again.lower() == 'y':
        total_hours_worked, gross_pay, fica_tax, net_pay = calculate_payroll()

        save_to_file = input("Would you like to save the payroll summary to a file? (y/n): ")
        if save_to_file.lower() == "y":
            name = input("Please enter the name: ")
            save_payroll(name, total_hours_worked, gross_pay, fica_tax, net_pay)
        
        calculate_again = input("Would you like to calculate another payroll? (y/n): ")

main()