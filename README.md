# Payroll Calculator

This is a simple payroll calculator written in Python. It allows you to manage employees and calculate their payroll based on the number of hours they've worked and their unique hourly wage.

## Features

- **Add Employee**: You can add a new employee to the system. You'll need to provide the employee's name, email, and hourly wage. Each employee is assigned a unique ID.

- **Edit Employee**: You can edit an existing employee's details. You'll need to provide the employee's ID and the new details you want to update.

- **Delete Employee**: You can delete an existing employee from the system. You'll need to provide the employee's ID. A confirmation is required to prevent accidental deletions.

- **Calculate Payroll**: You can calculate the payroll for an employee. You'll need to enter the employee's ID and the number of hours they've worked. The program will calculate the regular pay, overtime pay (if any), gross pay, FICA tax, and net pay. After calculating the payroll, a PDF timecard will be generated for the current payroll.

- **Search**: You can search for an employee using their ID. You can also search for all instances of a name, the total net pay, or list all employees.

## Usage

Run the program and follow the prompts. You can choose to add an employee, edit an employee, delete an employee, calculate payroll, or search for an employee. You can also exit the program.

When adding an employee, you'll be asked for the employee's name, email, and hourly wage. The employee will be assigned a unique ID.

When editing an employee, you'll be asked for the employee's ID and the new details you want to update.

When deleting an employee, you'll be asked for the employee's ID. A confirmation is required to prevent accidental deletions.

When calculating payroll, you'll be asked for the employee's ID and the number of hours they've worked. The program will calculate the regular pay, overtime pay (if any), gross pay, FICA tax, and net pay. After calculating the payroll, a PDF timecard will be generated for the current payroll and saved to a specified location.

When searching, you can choose to search for a specific employee using their ID, all instances of a name, the total net pay, or list all employees.

## Shortcuts

You can use the following shortcuts for the commands:

- Add: A
- Edit: E
- Delete: D
- Calculate: C
- Search: S
- Exit: X

## Future Improvements

- Improve the search functionality to allow searching by name or email.

## Setup

1. Ensure Python is installed on your system.
2. Download the `pay_calculator.py` file.
3. Create a Python virtual environment in the same directory as `pay_calculator.py` using the command: `python -m venv env`
4. Activate the virtual environment:
   - On Windows, run: `env\Scripts\activate`
   - On Unix or MacOS, run: `source env/bin/activate`
5. Install the required packages using the command: `pip install -r requirements.txt`
6. Install a LaTeX compiler on your system. This is required to generate the PDF time cards. We recommend using [TeX Live](https://www.tug.org/texlive/).
7. Create a `settings.json` file in the same directory as `pay_calculator.py`. This file should contain the paths to your payroll summary, employees files, and the directory for time cards. For example:

```json
{
  "payroll_summary_path": "payroll_summary.json",
  "employees_path": "employees.json",
  "time_cards_directory": "./time-cards"
}
```

The `payroll_summary_path`, `employees_path`, and `timecards_directory` are relative to the current project directory. For example, if `payroll_summary_path` is set to `"payroll_summary.json"`, the `pay_calculator.py` script will look for this file in the same directory where the script is located.

For the `timecards_directory`, you should include `./` at the start of the path to make it relative to the current project directory. For example, if `timecards_directory` is set to `"./timecards"`, the time cards will be saved in a timecards directory inside the current project directory.

## How to Run

1. Open a terminal or command prompt.
2. Navigate to the directory containing the script.
3. If not already activated, activate the virtual environment:
   - On Windows, run: `env\Scripts\activate`
   - On Unix or MacOS, run: `source env/bin/activate`
4. Run the script using the command: `python pay_calculator.py`.
5. Follow the on screen prompts to navigate the menu.

## Requirements

- Python 3.x
- LaTeX compiler (e.g., [TeX Live](https://www.tug.org/texlive/))

## Contribution

Contributions are welcome! Feel free to fork this repository and submit pull requests for any improvements or bug fixes.

## License

[MIT License](https://opensource.org/licenses/MIT) - This project is open-source and free to use.
