import json
import datetime
from collections import OrderedDict
from pylatex import Document, Section, Subsection, Tabular, MultiColumn, LongTable, Command
from pylatex.utils import bold
import click


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    if ctx.invoked_subcommand is None:
        ctx.invoke(show_menu)


@cli.command()
@click.pass_context
def show_menu(ctx):
    while True:
        click.echo('1. Add Employee')
        click.echo('2. Calculate Payroll')
        click.echo('3. Delete Employee')
        click.echo('4. Edit Employee')
        click.echo('5. Search')
        click.echo('6. Exit')

        choice = click.prompt('Please enter a choice', type=int)

        if choice == 1:
            ctx.forward(add_employee)
        elif choice == 2:
            ctx.forward(calculate_payroll)
        elif choice == 3:
            ctx.forward(delete_employee)
        elif choice == 4:
            ctx.forward(edit_employee)
        elif choice == 5:
            ctx.forward(search)
        elif choice == 6:
            break
        else:
            click.echo('Invalid choice')


@click.group()
def search():
    pass


def load_settings():
    with open("settings.json", "r") as f:
        return json.load(f)


settings = load_settings()

file_path = settings["payroll_summary_path"]
employees_path = settings["employees_path"]


def save_employees(employees, employees_path):
    """
    Save the list of employees to a JSON file.

    Args:
        employees (list): A list of employee objects.
        employees_path (str): The path to the JSON file.

    Returns:
        None
    """
    with open(employees_path, "w") as f:
        json.dump(employees, f)


def load_employees(employees_path):
    """
    Load the list of employees from a JSON file.

    Args:
        employees_path (str): The path to the JSON file.

    Returns:
        dict: A dictionary of employees, or an empty dictionary if the file does not exist.
    """
    try:
        with open(employees_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print("The file was not found, initializing an empty list of employees.")
        return {}
    except json.JSONDecodeError:
        print("JSON decoding failed, initializing an empty list of employees.")
        return {}
    except PermissionError:
        print("Permission denied while trying to read the file.")
        return {}


def calculate_overtime(total_hours_worked, hours_worked, hourly_wage):
    """
    Calculates the overtime hours and pay.

    Args:
        total_hours_worked (float): The total hours worked so far.
        hours_worked (float): The hours worked in the current period.
        hourly_wage (float): The hourly wage.

    Returns:
        tuple: A tuple containing the new total hours worked, the overtime hours, and the overtime pay.
    """
    if total_hours_worked + hours_worked > 40:
        overtime_hours = (total_hours_worked + hours_worked) - 40
    else:
        overtime_hours = 0

    total_hours_worked += hours_worked

    # Calculate the overtime wage
    overtime_wage = hourly_wage * 1.5

    # Calculate the overtime pay
    overtime_pay = overtime_hours * overtime_wage

    return total_hours_worked, overtime_hours, overtime_pay


@cli.command()
@click.option('--employee_id', prompt='Employee ID', type=str, help='The ID of the employee.')
def calculate_payroll(employee_id):
    """
    Calculates the payroll summary based on the number of hours worked and hourly wage.

    Returns:
        A tuple containing the total hours worked, gross pay, FICA tax, and net pay.
    """
    try:
        employees = load_employees(
            employees_path)  # Load employees from the JSON file

        # Check if the employee ID exists
        if employee_id not in employees:
            click.echo("Invalid employee ID.")
            return

        hourly_wage = employees[employee_id]["hourly_wage"]

        # Initialize the hours worked
        total_hours_worked = 0.0
        overtime_hours = 0.0

        while True:
            # Ask the user for the number of hours worked
            while True:
                hours_worked = click.prompt(
                    "Please enter the number of hours worked (or 'done' to finish)", type=str)
                if hours_worked.lower() == "done":
                    break
                try:
                    hours_worked = float(hours_worked)
                    total_hours_worked, overtime_hours, overtime_pay = calculate_overtime(
                        total_hours_worked, hours_worked, hourly_wage)

                    # Calculate the FICA tax
                    fica_tax_rate = 7.65 / 100

                    # Calculate the gross pay, FICA tax, and net pay
                    if total_hours_worked > 40:
                        regular_hours = 40
                    else:
                        regular_hours = total_hours_worked

                    gross_pay = (regular_hours * hourly_wage) + overtime_pay
                    fica_tax = gross_pay * fica_tax_rate
                    net_pay = gross_pay - fica_tax

                except ValueError:
                    click.echo(
                        "Invalid input. Please enter a valid number of hours.")

            if hours_worked.lower() == "done":
                break

        # Print the total hours worked
        click.echo("\nPayroll Summary")
        click.echo("-------------------------")
        click.echo(f"Total Hours Worked: {total_hours_worked:.2f}")

        # Print the overtime hours if any
        if overtime_hours > 0:
            click.echo(f"Overtime Hours: {overtime_hours:.2f}")
            click.echo(
                f"Overtime Pay ({overtime_hours} * ${hourly_wage * 1.5:.2f}): ${overtime_pay:.2f}"
            )

        # Print the gross pay, FICA tax, and net pay
        if overtime_hours > 0:
            click.echo(
                f"Gross Pay ({total_hours_worked - overtime_hours} * ${hourly_wage:.2f} + ${overtime_pay:.2f}): ${gross_pay:.2f}"
            )
        else:
            click.echo(
                f"Gross Pay ({total_hours_worked - overtime_hours} * ${hourly_wage:.2f}): ${gross_pay:.2f}"
            )
        click.echo(
            f"FICA Tax (${gross_pay:.2f} * {fica_tax_rate}): ${fica_tax:.2f}")
        click.echo(
            f"Net Pay (${gross_pay:.2f} - ${fica_tax:.2f}): ${net_pay:.2f}")

        click.echo("-------------------------")

    except ValueError:
        click.echo("\nInvalid input. Please enter a valid number of hours.\n")

    return (
        total_hours_worked,
        overtime_hours,
        overtime_pay,
        gross_pay,
        fica_tax,
        net_pay,
    )


def generate_time_card(employee, total_hours_worked, wage_details):
    """
    Generates a time card document for an employee.

    Args:
        employee (dict): Dictionary containing employee details.
        total_hours_worked (float): Total hours worked by the employee.
        wage_details (dict): Dictionary containing wage details.

    Returns:
        None
    """
    doc = Document("time_card")

    doc.preamble.append(Command('title', 'Time Card'))
    doc.preamble.append(Command('author', employee['name']))
    doc.preamble.append(Command('date', ''))
    doc.append(Command('maketitle'))

    with doc.create(Section('Employee Details')):
        employee_details = Tabular('l l')
        employee_details.add_row(("Name:", employee['name']))
        employee_details.add_row(
            ("Hourly Wage:", f"${employee['hourly_wage']:.2f}"))
        doc.append(employee_details)

    with doc.create(Section('Worked Hours')):
        doc.append(f"Total Hours Worked: {total_hours_worked}")

    with doc.create(Section('Wage Details')):
        table = Tabular('l r')
        table.add_row(("Gross Pay", f"${wage_details['gross_pay']:.2f}"))
        table.add_row(("FICA Tax", f"${wage_details['fica_tax']:.2f}"))
        table.add_row(("Net Pay", f"${wage_details['net_pay']:.2f}"))
        doc.append(table)

    doc.generate_pdf(clean_tex=False)


def save_payroll(
    name, total_hours_worked, overtime_hours, overtime_pay, gross_pay, fica_tax, net_pay
):
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
        payroll_summary = OrderedDict(
            [
                ("Name", name),
                ("Date", datetime.datetime.now().strftime("%Y-%m-%d")),
                ("Total Hours", total_hours_worked),
                ("Gross Pay", round(gross_pay, 2)),
                ("FICA Tax", round(fica_tax, 2)),
                ("Net Pay", round(net_pay, 2)),
            ]
        )

        if overtime_hours > 0:
            # Add Overtime Hours and Overtime Pay to the end of the dictionary
            payroll_summary["Overtime Hours"] = overtime_hours
            payroll_summary["Overtime Pay"] = round(overtime_pay, 2)

            # Move Gross Pay, FICA Tax, and Net Pay to the end of the dictionary
            for key in ["Gross Pay", "FICA Tax", "Net Pay"]:
                payroll_summary.move_to_end(key)

        # Generate time card
        employee = {"name": name,
                    "hourly_wage": gross_pay / total_hours_worked}
        wage_details = {
            "gross_pay": gross_pay,
            "fica_tax": fica_tax,
            "net_pay": net_pay,
        }
        generate_time_card(employee, total_hours_worked, wage_details)

        # Read the existing data from the file
        try:
            with open(file_path, "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            print("\nError: Payroll summary file not found.\n")
            data = []
        except json.JSONDecodeError:
            print("\nError: Invalid JSON format in payroll summary file.\n")
            data = []

        # Append the new payroll summary
        data.append(payroll_summary)

        # Write the data back to the file
        try:
            with open(file_path, "w") as file:
                json.dump(data, file, indent=4)
        except PermissionError:
            print(
                "\nError: Permission denied when trying to write to the payroll summary file.\n")
            return

        print("\nPayroll summary saved to payroll_summary.json\n")

    except Exception as e:
        print(f"\nUnexpected error occurred: {str(e)}\n")


@search.command()
@click.option('--file_path', prompt='File path', type=str, help='The path to the payroll summary file.')
@click.option('--name', prompt='Name', type=str, help='The name to search in the payroll summary.')
def search_payroll(file_path, name):
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
        except FileNotFoundError:
            click.echo("\nError: Payroll summary file not found.\n")
            data = []
        except json.JSONDecodeError:
            click.echo(
                "\nError: Invalid JSON format in payroll summary file.\n")
            data = []

        # Convert the name to lowercase for case insensitive search
        name = name.lower()

        # Search the payroll summary for the name
        found = False
        for payroll_summary in data:
            if payroll_summary["Name"].lower() == name:
                click.echo("-------------------------")
                click.echo(f"Name: {payroll_summary['Name']}")
                click.echo(f"Date: {payroll_summary['Date']}")
                click.echo(
                    f"Total Hours: {payroll_summary['Total Hours']} hrs")
                if "Overtime Hours" in payroll_summary:
                    click.echo(
                        f"Overtime Hours: {payroll_summary['Overtime Hours']} hrs")
                if "Overtime Pay" in payroll_summary:
                    click.echo(
                        f"Overtime Pay: ${payroll_summary['Overtime Pay']}")
                click.echo(f"Gross Pay: ${payroll_summary['Gross Pay']}")
                click.echo(f"FICA Tax: ${payroll_summary['FICA Tax']}")
                click.echo(f"Net Pay: ${payroll_summary['Net Pay']}")
                click.echo("-------------------------")
                found = True

        if not found:
            click.echo("\nNo payroll summary found for the specified name.\n")

    except Exception as e:
        click.echo(f"\nUnexpected error occurred: {str(e)}\n")


@search.command()
@click.option('--name', prompt='Name', type=str, help='The name to search in the payroll summary.')
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
        except FileNotFoundError:
            click.echo("\nError: Payroll summary file not found.\n")
            data = []
        except json.JSONDecodeError:
            click.echo(
                "\nError: Invalid JSON format in payroll summary file.\n")
            data = []

        # Convert the name to lowercase for case insensitive search
        name = name.lower()

        # Search the payroll summary for the name
        total_net_pay = 0.0
        for payroll_summary in data:
            if payroll_summary["Name"].lower() == name:
                total_net_pay += payroll_summary["Net Pay"]

        click.echo(f"\nTotal Net Pay: ${total_net_pay:.2f}\n")

    except Exception as e:
        click.echo(f"\nUnexpected error occurred: {str(e)}\n")


@search.command()
@click.option('--employee_id', prompt='Employee ID', type=str, help='The ID of the employee.')
def search_employee(employee_id):
    try:
        employees = load_employees(
            employees_path)  # Load employees from the JSON file

        # Check if the employee ID exists
        if employee_id not in employees:
            click.echo("\nEmployee not found.\n")
            return

        # Print the employee details
        click.echo("\nEmployee found:")
        click.echo(f"Name: {employees[employee_id]['name']}")
        click.echo(f"Email: {employees[employee_id]['email']}")
        click.echo(f"Hourly wage: {employees[employee_id]['hourly_wage']}\n")

    except Exception as e:
        click.echo(f"\nUnexpected error occurred: {str(e)}\n")


@search.command()
def list_employees():
    """
    Prints the details of each employee in the provided dictionary.

    Parameters:
    employees (dict): A dictionary containing employee information.

    Returns:
    None
    """
    try:
        # Load employees from the JSON file
        employees = load_employees(employees_path)

        click.echo("\n------------------------")
        for employee_id, employee_info in employees.items():
            click.echo(f"ID: {employee_id}")
            click.echo(f"Name: {employee_info['name']}")
            click.echo(f"Email: {employee_info['email']}")
            click.echo(f"Hourly wage: {employee_info['hourly_wage']}")
            click.echo("------------------------")
        click.echo()

    except Exception as e:
        click.echo(f"\nUnexpected error occurred: {str(e)}\n")


@cli.command()
@click.option('--id', prompt='Employee ID', help="The employee's ID")
@click.option('--name', prompt='Employee name', help="The employee's name")
@click.option('--email', prompt='Employee email', help="The employee's email")
@click.option('--wage', prompt='Employee wage', type=float, help="The employee's hourly wage")
def add_employee(id, name, email, wage):
    """
    Adds a new employee to the employee dictionary.

    Parameters:
    id (str): The employee's ID.
    name (str): The employee's name.
    email (str): The employee's email.
    wage (float): The employee's hourly wage.

    Returns:
    None
    """
    employees = load_employees(
        employees_path)  # Load employees from the JSON file
    if id in employees:
        click.echo("An employee with that ID already exists.")
    else:
        employees[id] = {
            "name": name,
            "email": email,
            "hourly_wage": wage
        }
        save_employees(employees, employees_path)
        click.echo(f'Adding employee: {name} with ID: {id}')


@cli.command()
@click.option('--id', prompt='Employee ID', help="The employee's ID")
def edit_employee(employee_id):
    """
    Edit the details of an employee.

    Args:
        employees (dict): A dictionary containing employee information.

    Returns:
        None
    """
    try:
        # Load employees from the JSON file
        employees = load_employees(employees_path)
        if employee_id in employees:
            click.echo("\nCurrent Employee Details:")
            click.echo(f"Name: {employees[employee_id]['name']}")
            click.echo(f"Email: {employees[employee_id]['email']}")
            click.echo(f"Hourly wage: {employees[employee_id]['hourly_wage']}")

            click.echo(
                "\nEnter new details (leave blank to keep current value)")
            name = click.prompt("Enter the employee's new name",
                                default=employees[employee_id]['name'], show_default=False)
            email = click.prompt("Enter the employee's new email",
                                 default=employees[employee_id]['email'], show_default=False)
            hourly_wage = click.prompt("Enter the employee's new hourly wage",
                                       default=employees[employee_id]['hourly_wage'], show_default=False)

            employees[employee_id]["name"] = name
            employees[employee_id]["email"] = email
            employees[employee_id]["hourly_wage"] = float(hourly_wage)

            # Save employees to the JSON file
            save_employees(employees, employees_path)
            click.echo("\nEmployee details updated.\n")
        else:
            click.echo("\nEmployee not found.\n")

    except Exception as e:
        click.echo(f"\nUnexpected error occurred: {str(e)}\n")


@cli.command()
@click.option('--id', prompt='Employee ID', help="The employee's ID")
def delete_employee(employee_id):
    """
    Deletes an employee from the employees dictionary based on the provided employee ID.

    Args:
        employees (dict): A dictionary containing employee information.

    Returns:
        None
    """
    try:
        # Load employees from the JSON file
        employees = load_employees(employees_path)
        if employee_id in employees:
            click.echo("Employee Details:")
            click.echo(f"Name: {employees[employee_id]['name']}")
            click.echo(f"Email: {employees[employee_id]['email']}")
            click.echo(f"Hourly wage: {employees[employee_id]['hourly_wage']}")

            confirm = click.prompt(
                "\nAre you sure you want to delete this employee? (Y/N)", type=str)
            if confirm.lower() in ["yes", "y"]:
                del employees[employee_id]
                # Save employees to the JSON file
                save_employees(employees, employees_path)
                click.echo("\nEmployee deleted.\n")
            else:
                click.echo("\nEmployee not deleted.\n")
        else:
            click.echo("\nEmployee not found.\n")
    except Exception as e:
        click.echo(f"\nUnexpected error occurred: {str(e)}\n")


def main():
    """
    The main function.
    """
    employees = load_employees(
        employees_path)  # Load employees from the JSON file

    exit_program = False

    while not exit_program:
        action = input(
            "Would you like to (A)dd an employee, (C)alculate payroll, (S)earch for an employee, (E)dit an employee, (D)elete an employee, or e(X)it? (A/C/S/E/D/X): "
        )

        if action.lower() in ["add", "a"]:
            add_employee(employees)

        elif action.lower() in ["calculate", "c"]:
            employee_id = input(
                "Enter the employee ID for whom you want to calculate payroll: "
            )
            if employee_id in employees:
                (
                    total_hours_worked,
                    overtime_hours,
                    overtime_pay,
                    gross_pay,
                    fica_tax,
                    net_pay,
                ) = calculate_payroll(employees[employee_id]["hourly_wage"])

                save_to_file = input(
                    "Would you like to save the payroll summary to a file? (y/n): "
                )
                if save_to_file.lower() == "y":
                    save_payroll(
                        employees[employee_id]["name"],
                        total_hours_worked,
                        overtime_hours,
                        overtime_pay,
                        gross_pay,
                        fica_tax,
                        net_pay,
                    )
            else:
                print("\nEmployee ID not found.\n")

        elif action.lower() in ["search", "s"]:
            search_type = input(
                "Would you like to search for a (S)pecific employee, (A)ll instances of a name, (T)otal net pay, or (L)ist all employees? (S/A/T/L): "
            )
            if search_type.lower() in ["specific", "s"]:
                search_employee(employees)
            elif search_type.lower() in ["all", "a"]:
                search_payroll()
            elif search_type.lower() in ["total", "t"]:
                total_net_pay_search()
            elif search_type.lower() in ["list", "l"]:
                list_employees(employees)
            else:
                print(
                    "\nInvalid command. Please enter 'specific', 'all', 'total', or 'list'.\n")

        elif action.lower() in ["edit", "e"]:
            edit_employee(employees)

        elif action.lower() in ["delete", "d"]:
            delete_employee(employees)

        elif action.lower() in ["exit", "x"]:
            exit_program = True

        else:
            print(
                "\nInvalid command. Please enter 'add', 'calculate', 'search', 'edit', 'delete', or 'exit'.\n"
            )


cli.add_command(search)

if __name__ == '__main__':
    cli()
