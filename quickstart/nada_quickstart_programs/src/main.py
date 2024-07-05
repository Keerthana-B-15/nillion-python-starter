from nada_dsl import *


def initialize_departments(nr_departments):
    """
    Initializes the list of departments with unique identifiers.

    Args:
    nr_departments (int): Number of departments.

    Returns:
    list: List of Party objects representing each department.
    """
    departments = []
    for i in range(nr_departments):
        departments.append(Party(name="Department" + str(i)))

    return departments


def inputs_initialization(nr_departments, nr_quarters, departments):
    """
    Initializes the input for each financial quarter, collecting expenses from each department securely.

    Args:
        nr_departments (int): Number of departments.
        nr_quarters (int): Number of financial quarters.

    Returns:
        list: List of lists containing SecretUnsignedInteger objects representing expenses per department per quarter.
    """
    expenses = []
    for q in range(nr_quarters):
        expenses.append([])
        for d in range(nr_departments):
            expenses[q].append(
                SecretUnsignedInteger(
                    Input(name="d" + str(d) + "_q" + str(q), party=departments[d])
                )
            )

    return expenses


def total_expenses(nr_departments, nr_quarters, expenses, outparty):
    """
    Calculates the total expenses for each financial quarter.

    Args:
        nr_departments (int): Number of departments.
        nr_quarters (int): Number of financial quarters.
        expenses (list): List of lists containing SecretUnsignedInteger objects representing expenses per department per quarter.

    Returns:
        list: List of Output objects representing the total expenses for each financial quarter.
    """
    total_expenses = []
    for q in range(nr_quarters):
        total_amount = expenses[q][0]
        for d in range(1, nr_departments):
            total_amount += expenses[q][d]
        total_expenses.append(Output(total_amount, "total_expenses_q" + str(q), outparty))

    return total_expenses


def fn_check_sum(nr_departments, nr_quarters, expenses, outparty):
    """
    Verifies the sum of expenses for each department across all quarters to ensure correctness.

    Args:
        nr_departments (int): Number of departments.
        nr_quarters (int): Number of financial quarters.
        expenses (list): List of lists containing SecretUnsignedInteger objects representing expenses per department per quarter.

    Returns:
        list: List of Output objects representing the sum verification for each department.
    """
    check_sum = []
    for d in range(nr_departments):
        check = expenses[0][d]
        for q in range(1, nr_quarters):
            amount_d_q = expenses[q][d]
            check += amount_d_q
        check_sum.append(Output(check, "check_sum_d" + str(d), outparty))

    return check_sum


def fn_check_consistency(nr_departments, nr_quarters, expenses, outparty):
    """
    Verifies the consistency of expenses across departments and quarters.

    Args:
        nr_departments (int): Number of departments.
        nr_quarters (int): Number of financial quarters.
        expenses (list): List of lists containing SecretUnsignedInteger objects representing expenses per department per quarter.

    Returns:
        list: List of Output objects representing the consistency verification for each department and quarter.
    """
    check_consistency = []
    for d in range(nr_departments):
        for q in range(nr_quarters):
            amount_d_q = expenses[q][d]
            check_d_q_consistency = (UnsignedInteger(1) - amount_d_q) * (
                UnsignedInteger(2) - amount_d_q
            )
            check_consistency.append(
                Output(
                    check_d_q_consistency, "check_consistency_d" + str(d) + "_q" + str(q), outparty
                )
            )

    return check_consistency


def nada_main():
    global nr_quarters  # Declare nr_quarters as global

    # Compiled-time constants
    nr_departments = 4
    nr_quarters = 3

    # Parties initialization
    departments = initialize_departments(nr_departments)
    outparty = Party(name="OutParty")

    # Inputs initialization
    expenses = inputs_initialization(nr_departments, nr_quarters, departments)

    # Computation
    total_expenses_output = total_expenses(nr_departments, nr_quarters, expenses, outparty)
    check_sum_output = fn_check_sum(nr_departments, nr_quarters, expenses, outparty)
    check_consistency_output = fn_check_consistency(nr_departments, nr_quarters, expenses, outparty)

    # Output
    results = total_expenses_output + check_sum_output + check_consistency_output
    return results


if __name__ == "__main__":
    # Run the NaDA program
    outputs = nada_main()

    # Print the outputs
    for i, output in enumerate(outputs):
        if i < len(outputs) // 3:
            print(f"Output {i + 1}: Total expenses for Quarter {i}: {output}")
        elif i < 2 * (len(outputs) // 3):
            print(f"Output {i + 1}: Sum verification for Department {i - len(outputs) // 3}: {output}")
        else:
            department_idx = (i - 2 * (len(outputs) // 3)) // nr_quarters
            quarter_idx = (i - 2 * (len(outputs) // 3)) % nr_quarters
            print(f"Output {i + 1}: Consistency check for Department {department_idx} in Quarter {quarter_idx}: {output}")
