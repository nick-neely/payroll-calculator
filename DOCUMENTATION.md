# Payroll Calculator Documentation

## Overview
`pay_calculator.py` is a Python script that serves as a payroll calculation and management system. It provides functionality to manage employee details, calculate payroll, and generate time card documents. The program operates through a command-line interface, allowing users to interact with the system by adding, editing, or deleting employee information, calculating payroll based on hours worked, and generating a time card PDF for record-keeping.

## Features
- Add new employees to the system with details such as name, email, and hourly wage.
- Edit existing employee details.
- Delete employees from the system.
- List all employees with their details.
- Calculate payroll for employees, which includes handling regular and overtime pay, and calculating FICA taxes and net pay.
- Generate a time card PDF document for an employee with details of hours worked and wage calculations.
- Save payroll summaries to a JSON file for persistence.
- Search functionality to find employees by ID or name, and calculate total net pay for an individual.

## Main Functionalities
- `add_employee(employees)`: Adds a new employee to the system by taking their ID, name, email, and hourly wage as input.
- `edit_employee(employees)`: Edits the details of an existing employee identified by their ID.
- `delete_employee(employees)`: Deletes an employee from the system based on the provided employee ID.
- `list_employees(employees)`: Lists all employees and their details stored in the system.
- `calculate_payroll(hourly_wage)`: Calculates payroll details such as total hours worked, gross pay, FICA tax, and net pay.
- `generate_time_card(employee, total_hours_worked, wage_details)`: Generates a PDF time card document for an employee.
- `save_payroll(name, total_hours_worked, overtime_hours, overtime_pay, gross_pay, fica_tax, net_pay)`: Saves the payroll summary to a JSON file.
- `search_payroll()`: Searches the payroll summary for a specific name.
- `total_net_pay_search()`: Searches the payroll summary for a given name and calculates the total net pay.
- `search_employee(employees)`: Searches for an employee by their ID and displays their details.

## Error Handling
The script includes basic error handling for file I/O operations and validates user input to prevent common errors. For example, it catches `FileNotFoundError` and `json.JSONDecodeError` when attempting to read or write to JSON files.

## Data Storage
Employee and payroll data are stored in JSON files. The script reads from and writes to these files to persist data across sessions.

## User Interaction
The script utilizes a simple text-based interface where the user inputs commands to interact with the system. It guides the user through the available actions, such as adding an employee or calculating payroll.

## Limitations
- The system is currently designed for use in a command-line environment, which may not be as user-friendly as a graphical interface.
- Data validation is basic and may need enhancement to handle more complex validation requirements.
- The system is not designed for high-volume data and does not use a database, which could be a limitation for scalability.

## Potential Improvements
- Enhancing the user interface with a third-party library like `click` or `argparse` to make it more intuitive.
- Migrating data storage to a database for scalability and advanced data manipulation.
- Implementing a more robust error handling and logging system for better fault tolerance and debugging.
- Refactoring the code to improve modularity and maintainability.
