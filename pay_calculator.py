import json
import datetime
from collections import OrderedDict

file_path = r"payroll_summary.json"

# Define the hourly wage
hourly_wage = 20.0


def calculate_payroll():
    """
    Calculates the payroll summary based on the number of hours worked and hourly wage.

    Returns:
        A tuple containing the total hours worked, gross pay, FICA tax, and net pay.
    """
    try:
        # Initialize the hours worked
        total_hours_worked = 0.0
        overtime_hours = 0.0

        while True:
            # Ask the user for the number of hours worked
            while True:
                hours_worked = input("Please enter the number of hours worked (or 'done' to finish): ")
                if hours_worked.lower() == 'done':
                    break
                try:
                    hours_worked = float(hours_worked)

                    if total_hours_worked + hours_worked > 40:
                        overtime_hours = (total_hours_worked + hours_worked) - 40
                    else:
                        overtime_hours = 0

                    total_hours_worked += hours_worked

                    # Calculate the overtime wage
                    overtime_wage = hourly_wage * 1.5

                    # Calculate the overtime pay
                    overtime_pay = overtime_hours * overtime_wage

                    # Calculate the FICA tax
                    fica_tax_rate = 7.65 / 100

                    # Calculate the gross pay, FICA tax, and net pay
                    gross_pay = (total_hours_worked * hourly_wage) + (overtime_hours * hourly_wage * 1.5)
                    fica_tax = gross_pay * fica_tax_rate
                    net_pay = gross_pay - fica_tax

                    # Calculate the net pay
                    net_pay = gross_pay - fica_tax

                except ValueError:
                    print("Invalid input. Please enter a valid number of hours.")
            
            if hours_worked.lower() == 'done':
                break
                    

        # Print the total hours worked
        print("\nPayroll Summary")
        print("-------------------------")
        print(f"Total Hours Worked: {total_hours_worked:.2f}")

        # Print the overtime hours if any
        if overtime_hours > 0:
            print(f"Overtime Hours: {overtime_hours:.2f}")
            print(f"Overtime Pay ({overtime_hours} * ${overtime_wage:.2f}): ${overtime_pay:.2f}")

        # Print the gross pay, FICA tax, and net pay
        if overtime_hours > 0:
            print(f"Gross Pay ({total_hours_worked - overtime_hours} * ${hourly_wage:.2f} + ${overtime_pay:.2f}): ${gross_pay:.2f}")
        else:
            print(f"Gross Pay ({total_hours_worked - overtime_hours} * ${hourly_wage:.2f}): ${gross_pay:.2f}")
        print(f"FICA Tax (${gross_pay:.2f} * {fica_tax_rate}): ${fica_tax:.2f}")
        print(f"Net Pay (${gross_pay:.2f} - ${fica_tax:.2f}): ${net_pay:.2f}")

        print("-------------------------")

    except ValueError:
        print("Invalid input. Please enter a valid number of hours.")

    return total_hours_worked, overtime_hours, overtime_pay, gross_pay, fica_tax, net_pay


def save_payroll(name, total_hours_worked, overtime_hours, overtime_pay, gross_pay, fica_tax, net_pay):
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
        payroll_summary = OrderedDict([
            ("Name", name),
            ("Date", datetime.datetime.now().strftime("%Y-%m-%d")),
            ("Total Hours", total_hours_worked),
            ("Gross Pay", round(gross_pay, 2)),
            ("FICA Tax", round(fica_tax, 2)),
            ("Net Pay", round(net_pay, 2))
        ])

        if overtime_hours > 0:
            # Add "Overtime Hours" and "Overtime Pay" to the end of the dictionary
            payroll_summary["Overtime Hours"] = overtime_hours
            payroll_summary["Overtime Pay"] = round(overtime_pay, 2)

            # Move "Gross Pay", "FICA Tax", and "Net Pay" to the end of the dictionary
            for key in ["Gross Pay", "FICA Tax", "Net Pay"]:
                payroll_summary.move_to_end(key)

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

def search_payroll():
    """
    Search the payroll summary for a specific name.

    Raises:
        IOError: If there is an error reading the payroll summary from the file.
    """
    try:
        # Read the existing data from the file
        try:
            with open(file_path, "r") as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            data = []

        # Ask the user for the name to search
        name = input("Please enter the name to search: ").lower()

        # Search the payroll summary for the name
        found = False
        for payroll_summary in data:
            if payroll_summary["Name"].lower() == name:
                print("-------------------------")
                print(f"Name: {payroll_summary['Name']}")
                print(f"Date: {payroll_summary['Date']}")
                print(f"Total Hours: {payroll_summary['Total Hours']} hrs")
                if "Overtime Hours" in payroll_summary:
                    print(f"Overtime Hours: {payroll_summary['Overtime Hours']} hrs")
                if "Overtime Pay" in payroll_summary:
                    print(f"Overtime Pay: ${payroll_summary['Overtime Pay']}")
                print(f"Gross Pay: ${payroll_summary['Gross Pay']}")
                print(f"FICA Tax: ${payroll_summary['FICA Tax']}")
                print(f"Net Pay: ${payroll_summary['Net Pay']}")
                print("-------------------------")
                found = True

        if not found:
            print("No payroll summary found for the specified name.")

    except IOError:
        print("Error reading payroll summary from file.")
    

def total_net_pay_search():
    """
    Searches the payroll summary for a given name and calculates the total net pay.

    Returns:
    None
    """
    try:
        # Read the existing data from the file
        try:
            with open(file_path, "r") as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            data = []

        # Ask the user for the name to search
        name = input("Please enter the name to search: ").lower()

        # Search the payroll summary for the name
        total_net_pay = 0.0
        for payroll_summary in data:
            if payroll_summary["Name"].lower() == name:
                total_net_pay += payroll_summary["Net Pay"]

        print(f"Total Net Pay: ${total_net_pay:.2f}")

    except IOError:
        print("Error reading payroll summary from file.")

def main():
    """
    The main function.
    """
    exit_program = False

    while not exit_program:
        action = input("Would you like to calculate payroll, search for an employee, or exit? (calculate/search/exit): ")

        if action.lower() == 'calculate':
            calculate_again = 'y'
            while calculate_again.lower() == 'y':
                total_hours_worked, overtime_hours, overtime_pay, gross_pay, fica_tax, net_pay = calculate_payroll()

                save_to_file = input("Would you like to save the payroll summary to a file? (y/n): ")
                if save_to_file.lower() == "y":
                    name = input("Please enter the name: ")
                    save_payroll(name, total_hours_worked, overtime_hours, overtime_pay, gross_pay, fica_tax, net_pay)
                
                calculate_again = input("Would you like to calculate another payroll? (y/n): ")

        elif action.lower() == 'search':
            search_name = input("Would you like to search for all instances of a name? (y/n): ")
            if search_name.lower() == "y":
                search_payroll()

            search_net_pay = input("Would you like to calculate the total net pay for a name? (y/n): ")
            if search_net_pay.lower() == "y":
                total_net_pay_search()
        
        elif action.lower() == 'exit':
            exit_program = True

        else:
            print("Invalid command. Please enter 'calculate', 'search', or 'exit'.")

main()