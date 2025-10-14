def convert_pay_string_to_number(pay_string):
    """
    Converts a pay string like '$100' (in millions) to a number of
    dollars.

    >>> convert_pay_string_to_number("$100 ")
    100000000.0
    """
    converted_pay_string = 10 ** 6 * float(pay_string.strip("$"))
    return converted_pay_string

my_str = '$53.25'
print(convert_pay_string_to_number(my_str))