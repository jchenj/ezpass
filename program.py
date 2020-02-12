"""
Define the function password_manager that takes one argument, account_name
    # Validate arguments
    If account_name not in Account col of spreadsheet,
        throw error with message "account_name not in spreadsheet"
    # Get password
    If cell [row with account_name][password column] is empty,
        throw error with message "no password entered for account_name"
    # Copy password
    Copy contents of cell [row with account_name][password column] to paste buffer
    Print message "Password for account_name in print_buffer"
"""